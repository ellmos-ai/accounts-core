# SPDX-License-Identifier: MIT
"""Account domain core: bank accounts, CAMT balance import, and a privacy-safe
read-only projection for other consumers (e.g. OCEAN).

Extracted from BACH (the raw SQL of the ``/api/financial/bank-accounts``
endpoints in ``gui/server.py`` plus ``hub/steuer.py::_persist_camt_balances``)
as wave 1 of the account domain cut (decision D-20260903-003 = A, analysis
``KONTEN-DOMAENE-OCEAN-ANALYSE_2026-09-03.md``).

Contract (same as ``assistant-core``, the wave-1 sibling module):

* **One data canon.** The module never owns tables. ``AccountStore`` is handed
  a SQLite path (the consumer's ``bach.db``); it reads and writes the existing
  ``bank_accounts`` table and creates nothing.
* **No UI toolkit, no HTTP, no XML parsing.** Consumers wire their endpoints
  against this API and hand ``persist_camt_balances`` already-parsed balance
  dicts (the shape BACH's ``CamtParser.parse_balances()`` returns) -- the CAMT
  file format itself stays a BACH-side concern.
* **Behaviour identical to BACH.** Every statement below is the one BACH ran
  before the extraction; only the call site moved.

``credits`` (Kredite) is a related but separate domain per the analysis doc
and is intentionally NOT part of wave 1 -- it is not consumed by the CAMT
import or the transit projection, and BACH's own analysis treats it as its
own thing. Add it in a later wave if a consumer needs it.
"""
from __future__ import annotations

import os
import sqlite3

DB_ENV = "BACH_DB"

# Allowlist for the read-only transit projection (accounts.transit). Bank
# identifiers (account number, BIC, holder name, bank name, notes) never
# leave the module boundary -- only these five fields do, and IBAN only in
# masked form. Built as an explicit allowlist, never by deleting keys from
# the source row: a denylist forgets the next column someone adds to
# bank_accounts, and that column could be a bank identifier.
TRANSIT_FIELDS = ("name", "account_type", "balance", "balance_date", "iban_masked")


def default_db_path() -> str | None:
    """The consumer's canonical database, if it announced one via ``BACH_DB``.

    Same seam as ``assistant_core.default_db_path()``: reads the environment
    variable only, never guesses a path of its own.
    """
    value = os.environ.get(DB_ENV, "").strip()
    return value or None


def mask_iban(iban: str | None) -> str | None:
    """Keep only the last 4 characters of an IBAN; the rest becomes '*'.

    None/empty in, None out -- no placeholder that could be mistaken for data.
    """
    if not iban:
        return None
    cleaned = iban.replace(" ", "").upper()
    if len(cleaned) <= 4:
        return "*" * len(cleaned)
    return "*" * (len(cleaned) - 4) + cleaned[-4:]


def to_transit_row(account: dict) -> dict:
    """Project one ``bank_accounts`` row to the allowed transit fields.

    Allowlist, not denylist: the return value is built field by field from
    ``TRANSIT_FIELDS``. An unknown/new column on ``account`` (e.g. someone
    adds ``account_number`` or a new bank identifier to the source table)
    cannot leak through -- it was never named here.
    """
    return {
        "name": account.get("name"),
        "account_type": account.get("account_type"),
        "balance": account.get("balance"),
        "balance_date": account.get("balance_date"),
        "iban_masked": mask_iban(account.get("iban")),
    }


class AccountStore:
    """All reads and writes on the consumer's ``bank_accounts`` table."""

    def __init__(self, db_path: str | os.PathLike[str], timeout: float = 10.0) -> None:
        self.db_path = os.fspath(db_path)
        self.timeout = timeout

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=self.timeout)
        conn.row_factory = sqlite3.Row
        return conn

    # -- GUI semantics (formerly raw SQL in gui/server.py) ----------------

    def list_accounts(self) -> list[dict]:
        with self.connect() as conn:
            rows = conn.execute("SELECT * FROM bank_accounts ORDER BY name").fetchall()
            return [dict(row) for row in rows]

    def create_account(self, name: str, bank_name: str | None = None, iban: str | None = None,
                        bic: str | None = None, account_type: str = "girokonto",
                        notes: str | None = None) -> int:
        with self.connect() as conn:
            cur = conn.execute(
                "INSERT INTO bank_accounts (name, bank_name, iban, bic, account_type, notes) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (name, bank_name, iban, bic, account_type, notes),
            )
            return int(cur.lastrowid or 0)

    def update_account(self, account_id: int, name: str, bank_name: str | None = None,
                        iban: str | None = None, bic: str | None = None,
                        account_type: str = "girokonto", notes: str | None = None) -> None:
        with self.connect() as conn:
            conn.execute(
                "UPDATE bank_accounts SET "
                "name = ?, bank_name = ?, iban = ?, bic = ?, "
                "account_type = ?, notes = ?, updated_at = CURRENT_TIMESTAMP "
                "WHERE id = ?",
                (name, bank_name, iban, bic, account_type, notes, account_id),
            )

    def delete_account(self, account_id: int) -> None:
        with self.connect() as conn:
            conn.execute("DELETE FROM bank_accounts WHERE id = ?", (account_id,))

    # -- CAMT import semantics (formerly hub/steuer.py::_persist_camt_balances) --

    def persist_camt_balances(self, balances: list[dict]) -> list[str]:
        """UPSERT-by-normalized-IBAN, identical to BACH's ``_persist_camt_balances``.

        ``balances`` matches ``CamtParser.parse_balances()``'s shape:
        ``[{"iban": ..., "balance": ..., "currency": ..., "date": ...}, ...]``.
        Returns human-readable log lines, same wording as BACH.
        """
        if not balances:
            return ["[WARN] Keine Salden in der Datei - bank_accounts unveraendert."]
        lines = []
        with self.connect() as conn:
            for bal in balances:
                iban_norm = (bal.get("iban") or "").replace(" ", "").upper()
                if not iban_norm or iban_norm == "UNKNOWN":
                    lines.append("[WARN] Saldo ohne IBAN uebersprungen.")
                    continue
                row = conn.execute(
                    "SELECT id FROM bank_accounts WHERE REPLACE(UPPER(COALESCE(iban,'')),' ','')=?",
                    (iban_norm,),
                ).fetchone()
                waehrung = bal.get("currency") or "EUR"
                if row:
                    conn.execute(
                        "UPDATE bank_accounts SET balance=?, balance_date=?, "
                        "updated_at=datetime('now') WHERE id=?",
                        (bal["balance"], bal.get("date"), row["id"]),
                    )
                    lines.append(
                        f"[OK] Konto {iban_norm}: Saldo {bal['balance']:.2f} "
                        f"{waehrung} zum {bal.get('date')} aktualisiert."
                    )
                else:
                    conn.execute(
                        "INSERT INTO bank_accounts (name, iban, balance, balance_date) "
                        "VALUES (?,?,?,?)",
                        (f"CAMT-Import {iban_norm}", iban_norm, bal["balance"], bal.get("date")),
                    )
                    lines.append(
                        f"[OK] Konto {iban_norm} neu angelegt, Saldo "
                        f"{bal['balance']:.2f} {waehrung} zum {bal.get('date')} "
                        f"(Name via GUI editierbar)."
                    )
        return lines

    # -- read-only transit projection --------------------------------------

    def transit_projection(self) -> list[dict]:
        """Allowlist projection of all accounts for read-only consumers (OCEAN)."""
        return [to_transit_row(account) for account in self.list_accounts()]
