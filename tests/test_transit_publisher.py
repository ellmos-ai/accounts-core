# SPDX-License-Identifier: MIT
from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone

import pytest

from accounts_core import publish_transit_projection
from test_accounts import BACH_BANK_ACCOUNTS_DDL


@pytest.fixture
def source_db(tmp_path):
    path = tmp_path / "bach.db"
    with sqlite3.connect(path) as connection:
        connection.executescript(BACH_BANK_ACCOUNTS_DDL)
        connection.execute(
            "INSERT INTO bank_accounts "
            "(name, account_number, bank_name, iban, bic, holder_name, account_type, balance, balance_date, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "CAMT-Import DE89370400440532013000",
                "0532013000",
                "Private Bank",
                "DE89370400440532013000",
                "COBADEFFXXX",
                "Private Person",
                "girokonto",
                1234.5,
                "2026-09-09",
                "private note",
            ),
        )
    return path


def test_publisher_is_read_only_and_emits_only_the_contract_allowlist(source_db, tmp_path):
    output = tmp_path / "accounts.sqlite"
    checkpoint = tmp_path / "checkpoint.json"
    source_before = hashlib.sha256(source_db.read_bytes()).hexdigest()

    report = publish_transit_projection(
        source_db,
        output,
        checkpoint,
        publisher_instance="bach-primary",
        now=datetime(2026, 9, 9, 6, 45, tzinfo=timezone.utc),
        salt="a" * 32,
    )

    assert hashlib.sha256(source_db.read_bytes()).hexdigest() == source_before
    assert report["record_count"] == 1
    assert report["complete_snapshot"] is True
    with sqlite3.connect(output) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
        }
        assert tables == {"projection_metadata", "account_balances", "projection_tombstones"}
        row = connection.execute("SELECT * FROM account_balances").fetchone()
        columns = [item[0] for item in connection.execute("SELECT * FROM account_balances").description]
        payload = dict(zip(columns, row, strict=True))
    assert set(payload) == {
        "record_ref",
        "name",
        "account_type",
        "balance",
        "balance_date",
        "iban_masked",
        "record_version",
        "source_checkpoint",
        "publisher_instance",
    }
    assert payload["record_ref"] == hashlib.sha256(f"{'a' * 32}|bank_accounts|1".encode()).hexdigest()
    assert payload["name"] == "CAMT-Import " + "*" * 18 + "3000"
    assert payload["balance"] == "1234.50"
    assert payload["iban_masked"] == "*" * 18 + "3000"
    raw = output.read_bytes()
    for forbidden in (
        b"DE89370400440532013000",
        b"0532013000",
        b"Private Bank",
        b"COBADEFFXXX",
        b"Private Person",
        b"private note",
    ):
        assert forbidden not in raw


def test_complete_snapshot_advances_checkpoint_without_writing_source(source_db, tmp_path):
    output = tmp_path / "accounts.sqlite"
    checkpoint = tmp_path / "checkpoint.json"
    first = publish_transit_projection(
        source_db, output, checkpoint, publisher_instance="bach-primary", salt="b" * 32
    )
    second = publish_transit_projection(source_db, output, checkpoint, publisher_instance="bach-primary")
    assert first["source_checkpoint"] == 1
    assert second["source_checkpoint"] == 2
    assert json.loads(checkpoint.read_text(encoding="utf-8")) == {
        "checkpoint": 2,
        "salt": "b" * 32,
    }
    with sqlite3.connect(output) as connection:
        assert connection.execute("SELECT source_checkpoint FROM account_balances").fetchone() == (2,)


def test_missing_source_and_unsafe_path_aliases_fail_closed(tmp_path):
    missing = tmp_path / "missing.db"
    output = tmp_path / "out.sqlite"
    checkpoint = tmp_path / "checkpoint.json"
    with pytest.raises(FileNotFoundError):
        publish_transit_projection(missing, output, checkpoint, publisher_instance="bach-primary")

    source = tmp_path / "source.db"
    source.touch()
    with pytest.raises(ValueError, match="distinct"):
        publish_transit_projection(source, source, checkpoint, publisher_instance="bach-primary")
    with pytest.raises(ValueError, match="publisher_instance"):
        publish_transit_projection(source, output, checkpoint, publisher_instance="not valid!")
