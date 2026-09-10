# SPDX-License-Identifier: MIT
"""Application-owned publisher for the read-only OCEAN account projection.

The publisher reads BACH's canonical ``bank_accounts`` table through a
read-only SQLite connection and writes a separate, closed projection database.
Only the five fields from :data:`accounts_core.TRANSIT_FIELDS` leave the
module boundary. The source row id is used only as salted hash input and never
appears in the projection.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import sqlite3
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from .accounts import to_transit_row

CONTRACT_ID = "org.ellmos.accounts.balance-projection"
CONTRACT_VERSION = "1.0.0"
PUBLISHER_COMPONENT = "accounts-core-projection-adapter"

_PUBLISHER_INSTANCE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
_SALT_RE = re.compile(r"^[0-9a-f]{32,128}$")

_METADATA_DDL = """
CREATE TABLE projection_metadata (
    contract_id TEXT NOT NULL PRIMARY KEY,
    contract_version TEXT NOT NULL,
    publisher_component TEXT NOT NULL,
    publisher_instance TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    source_checkpoint INTEGER NOT NULL
)
"""
_ACCOUNTS_DDL = """
CREATE TABLE account_balances (
    record_ref TEXT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    account_type TEXT,
    balance TEXT,
    balance_date TEXT,
    iban_masked TEXT,
    record_version INTEGER NOT NULL,
    source_checkpoint INTEGER NOT NULL,
    publisher_instance TEXT NOT NULL
)
"""
_TOMBSTONES_DDL = """
CREATE TABLE projection_tombstones (
    record_type TEXT NOT NULL,
    record_ref TEXT NOT NULL,
    deleted_at TEXT NOT NULL,
    retain_until TEXT NOT NULL,
    record_version INTEGER NOT NULL,
    source_checkpoint INTEGER NOT NULL,
    publisher_instance TEXT NOT NULL,
    PRIMARY KEY (record_type, record_ref)
)
"""


def publish_transit_projection(
    source_db_path: str | os.PathLike[str],
    output_path: str | os.PathLike[str],
    checkpoint_path: str | os.PathLike[str],
    *,
    publisher_instance: str,
    now: datetime | None = None,
    salt: str | None = None,
) -> dict[str, Any]:
    """Publish one complete, privacy-allowlisted account snapshot.

    ``source_db_path`` is opened read-only. ``output_path`` and the publisher's
    small checkpoint file are replaced atomically and must be separate from the
    source. Every snapshot is complete, so a consumer replaces its previous
    view instead of merging absent rows or inferring tombstones.
    """
    if _PUBLISHER_INSTANCE_RE.fullmatch(publisher_instance) is None:
        raise ValueError(f"publisher_instance violates the contract: {publisher_instance!r}")

    source = Path(source_db_path).expanduser()
    output = Path(output_path).expanduser()
    checkpoint = Path(checkpoint_path).expanduser()
    _validate_distinct_paths(source, output, checkpoint)
    if not source.is_file():
        raise FileNotFoundError(f"Account source database does not exist: {source}")
    if not output.parent.is_dir() or not checkpoint.parent.is_dir():
        raise FileNotFoundError("Projection and checkpoint parent directories must already exist")

    state = _load_checkpoint(checkpoint)
    selected_salt = salt or state.get("salt") or secrets.token_hex(16)
    if not isinstance(selected_salt, str) or _SALT_RE.fullmatch(selected_salt) is None:
        raise ValueError("Publisher salt must be 32 to 128 lowercase hexadecimal characters")

    generated_at = _iso_utc(now or datetime.now(timezone.utc))
    source_checkpoint = state["checkpoint"] + 1
    rows = _read_projection_rows(source, selected_salt, source_checkpoint, publisher_instance)
    _write_projection(output, generated_at, source_checkpoint, publisher_instance, rows)
    _save_checkpoint(checkpoint, {"checkpoint": source_checkpoint, "salt": selected_salt})
    return {
        "status": "published-read-only-projection",
        "contract_id": CONTRACT_ID,
        "contract_version": CONTRACT_VERSION,
        "source_checkpoint": source_checkpoint,
        "generated_at": generated_at,
        "record_count": len(rows),
        "output_path": str(output),
        "complete_snapshot": True,
    }


def _validate_distinct_paths(source: Path, output: Path, checkpoint: Path) -> None:
    resolved = [path.resolve(strict=False) for path in (source, output, checkpoint)]
    if len(set(resolved)) != len(resolved):
        raise ValueError("Source, projection, and checkpoint paths must be distinct")


def _load_checkpoint(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"checkpoint": 0}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Invalid publisher checkpoint {path}: {error}") from error
    if not isinstance(payload, dict):
        raise ValueError("Publisher checkpoint must be a JSON object")
    value = payload.get("checkpoint")
    if type(value) is not int or value < 0:
        raise ValueError("Publisher checkpoint must contain a non-negative integer checkpoint")
    return payload


def _read_projection_rows(
    source: Path,
    salt: str,
    source_checkpoint: int,
    publisher_instance: str,
) -> list[dict[str, Any]]:
    connection = sqlite3.connect(f"file:{source.resolve().as_posix()}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only = ON")
    try:
        source_rows = connection.execute(
            "SELECT id, name, account_type, balance, balance_date, iban "
            "FROM bank_accounts ORDER BY name, id"
        ).fetchall()
    finally:
        connection.close()

    result = []
    for source_row in source_rows:
        projected = to_transit_row(dict(source_row))
        result.append(
            {
                "record_ref": hashlib.sha256(f"{salt}|bank_accounts|{source_row['id']}".encode()).hexdigest(),
                "name": projected["name"],
                "account_type": projected["account_type"],
                "balance": _canonical_balance(projected["balance"]),
                "balance_date": projected["balance_date"],
                "iban_masked": projected["iban_masked"],
                "record_version": source_checkpoint,
                "source_checkpoint": source_checkpoint,
                "publisher_instance": publisher_instance,
            }
        )
    return result


def _canonical_balance(value: Any) -> str | None:
    if value is None:
        return None
    try:
        return format(Decimal(str(value)).quantize(Decimal("0.01")), "f")
    except (InvalidOperation, ValueError) as error:
        raise ValueError(f"Account balance is not a finite decimal: {value!r}") from error


def _write_projection(
    output: Path,
    generated_at: str,
    source_checkpoint: int,
    publisher_instance: str,
    rows: list[dict[str, Any]],
) -> None:
    temporary = output.with_name(f".{output.name}.tmp-{os.getpid()}")
    if temporary.exists():
        temporary.unlink()
    connection: sqlite3.Connection | None = None
    try:
        connection = sqlite3.connect(temporary)
        connection.execute(_METADATA_DDL)
        connection.execute(_ACCOUNTS_DDL)
        connection.execute(_TOMBSTONES_DDL)
        connection.execute(
            "INSERT INTO projection_metadata VALUES (?, ?, ?, ?, ?, ?)",
            (
                CONTRACT_ID,
                CONTRACT_VERSION,
                PUBLISHER_COMPONENT,
                publisher_instance,
                generated_at,
                source_checkpoint,
            ),
        )
        columns = tuple(rows[0]) if rows else ()
        if columns:
            placeholders = ", ".join("?" for _ in columns)
            names = ", ".join(f'"{name}"' for name in columns)
            connection.executemany(
                f"INSERT INTO account_balances ({names}) VALUES ({placeholders})",
                [tuple(row[name] for name in columns) for row in rows],
            )
        connection.commit()
        result = connection.execute("PRAGMA quick_check").fetchone()
        if result is None or result[0] != "ok":
            raise sqlite3.DatabaseError(f"Projection quick_check failed: {result}")
    except Exception:
        if connection is not None:
            connection.close()
            connection = None
        temporary.unlink(missing_ok=True)
        raise
    finally:
        if connection is not None:
            connection.close()
    os.replace(temporary, output)


def _save_checkpoint(path: Path, state: dict[str, Any]) -> None:
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    payload = json.dumps(state, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    temporary.write_text(payload, encoding="utf-8")
    os.replace(temporary, path)


def _iso_utc(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("now must be timezone-aware")
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
