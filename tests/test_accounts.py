# SPDX-License-Identifier: MIT
"""Behavioural tests against the exact BACH ``bank_accounts`` DDL (schema.sql, main 6b6a038)."""
import sqlite3

import pytest

from accounts_core import (
    TRANSIT_FIELDS,
    AccountStore,
    default_db_path,
    mask_iban,
    to_transit_row,
)

BACH_BANK_ACCOUNTS_DDL = """
CREATE TABLE IF NOT EXISTS bank_accounts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    purpose TEXT,
    account_number TEXT,
    bank_name TEXT,
    blz TEXT,
    iban TEXT,
    bic TEXT,
    holder_name TEXT,
    account_type TEXT,
    is_primary INTEGER DEFAULT 0,
    balance REAL,
    balance_date TEXT,
    notes TEXT,
    dist_type INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_bank_accounts_iban ON bank_accounts(iban);
"""


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "bach.db"
    with sqlite3.connect(path) as conn:
        conn.executescript(BACH_BANK_ACCOUNTS_DDL)
    return str(path)


@pytest.fixture
def store(db_path):
    return AccountStore(db_path)


# -- AccountStore: identical to BACH's gui/server.py CRUD -------------------

def test_store_creates_no_tables(db_path):
    """One data canon: the module must never add schema to the consumer's DB."""
    before = _tables(db_path)
    AccountStore(db_path).list_accounts()
    assert _tables(db_path) == before == ["bank_accounts"]


def test_create_and_list_matches_bach_semantics(store):
    acc_id = store.create_account("Girokonto", bank_name="Sparkasse", iban="DE89370400440532013000",
                                   bic="COBADEFFXXX", account_type="girokonto", notes="Hauptkonto")
    accounts = store.list_accounts()
    assert len(accounts) == 1
    row = accounts[0]
    assert row["id"] == acc_id and row["name"] == "Girokonto" and row["bank_name"] == "Sparkasse"
    assert row["iban"] == "DE89370400440532013000" and row["bic"] == "COBADEFFXXX"
    assert row["account_type"] == "girokonto" and row["notes"] == "Hauptkonto"


def test_list_orders_by_name(store):
    store.create_account("Zweitkonto")
    store.create_account("Erstkonto")
    assert [a["name"] for a in store.list_accounts()] == ["Erstkonto", "Zweitkonto"]


def test_update_account(store):
    acc_id = store.create_account("Alt", bank_name="Bank A")
    store.update_account(acc_id, "Neu", bank_name="Bank B", iban="DE00", bic="X", notes="geaendert")
    row = store.list_accounts()[0]
    assert row["name"] == "Neu" and row["bank_name"] == "Bank B" and row["notes"] == "geaendert"


def test_delete_account(store):
    acc_id = store.create_account("Weg")
    store.delete_account(acc_id)
    assert store.list_accounts() == []


def test_default_db_path_reads_only_the_env(monkeypatch):
    monkeypatch.delenv("BACH_DB", raising=False)
    assert default_db_path() is None
    monkeypatch.setenv("BACH_DB", "  C:/somewhere/bach.db ")
    assert default_db_path() == "C:/somewhere/bach.db"


# -- CAMT import: identical UPSERT-by-normalized-IBAN to hub/steuer.py -----

def test_persist_camt_balances_updates_existing_account_by_normalized_iban(store):
    store.create_account("Girokonto", iban="DE89 3704 0044 0532 0130 00")
    lines = store.persist_camt_balances([
        {"iban": "de89370400440532013000", "balance": 1234.56, "currency": "EUR", "date": "2026-09-01"}
    ])
    row = store.list_accounts()[0]
    assert row["balance"] == 1234.56 and row["balance_date"] == "2026-09-01"
    assert "aktualisiert" in lines[0]


def test_persist_camt_balances_inserts_unknown_iban_as_new_account(store):
    lines = store.persist_camt_balances([
        {"iban": "DE12345678901234567890", "balance": 42.0, "currency": "EUR", "date": "2026-09-01"}
    ])
    row = store.list_accounts()[0]
    # Der Name landet ueber die Transit-Projektion bei OCEAN -- er darf die
    # IBAN nicht tragen (Review PR #18, P1).
    assert row["name"] == "CAMT-Import " + "*" * 18 + "7890"
    assert "DE12345678901234567890" not in row["name"]
    assert row["iban"] == "DE12345678901234567890" and row["balance"] == 42.0
    assert "neu angelegt" in lines[0]


def test_persist_camt_balances_skips_entries_without_iban(store):
    lines = store.persist_camt_balances([
        {"iban": "", "balance": 1.0, "date": "2026-09-01"},
        {"iban": "UNKNOWN", "balance": 2.0, "date": "2026-09-01"},
    ])
    assert store.list_accounts() == []
    assert lines == [
        "[WARN] Saldo ohne IBAN übersprungen.",
        "[WARN] Saldo ohne IBAN übersprungen.",
    ]


def test_persist_camt_balances_empty_list_warns_and_changes_nothing(store):
    lines = store.persist_camt_balances([])
    assert store.list_accounts() == []
    assert lines == ["[WARN] Keine Salden in der Datei - bank_accounts unverändert."]


# -- Allowlist projection: the field team-lead's brake is about -------------

def test_to_transit_row_contains_only_the_allowed_fields():
    row = to_transit_row({"name": "Girokonto", "account_type": "girokonto",
                           "balance": 10.0, "balance_date": "2026-09-01",
                           "iban": "DE89370400440532013000"})
    assert set(row.keys()) == set(TRANSIT_FIELDS)


def test_to_transit_row_drops_bank_identifiers_and_unknown_columns():
    """The exact test the brake demanded: a new, unknown source column must
    NOT leak through -- an allowlist ignores it, a denylist would forget it."""
    account = {
        "name": "Girokonto", "account_type": "girokonto",
        "balance": 10.0, "balance_date": "2026-09-01",
        "iban": "DE89370400440532013000",
        "account_number": "0532013000", "bic": "COBADEFFXXX",
        "bank_name": "Sparkasse", "holder_name": "Erika Musterfrau", "notes": "geheim",
        "brand_new_column_nobody_expected": "IBAN2-DE00-SECRET",
    }
    row = to_transit_row(account)
    assert set(row.keys()) == set(TRANSIT_FIELDS)
    for forbidden in ("account_number", "bic", "bank_name", "holder_name", "notes",
                      "brand_new_column_nobody_expected"):
        assert forbidden not in row
    assert "SECRET" not in str(row.values())


def test_to_transit_row_masks_iban_to_last_four_chars():
    row = to_transit_row({"iban": "DE89370400440532013000"})
    assert row["iban_masked"] == "*" * 18 + "3000"
    assert "DE89370400440532013000" not in row["iban_masked"]


def test_mask_iban_edge_cases():
    assert mask_iban(None) is None
    assert mask_iban("") is None
    assert mask_iban("AB") == "**"
    assert mask_iban("de89 3704 0044 0532 0130 00") == "*" * 18 + "3000"


def test_transit_projection_over_real_store(store):
    store.create_account("Girokonto", bank_name="Sparkasse", iban="DE89370400440532013000",
                          bic="COBADEFFXXX", account_type="girokonto", notes="Hauptkonto")
    projection = store.transit_projection()
    assert len(projection) == 1
    assert set(projection[0].keys()) == set(TRANSIT_FIELDS)
    assert projection[0]["name"] == "Girokonto"
    assert projection[0]["iban_masked"] == "*" * 18 + "3000"


def test_transit_projection_masks_an_iban_hidden_in_the_name(store):
    """`name` ist GUI-editierbar und trug bei Altzeilen die volle IBAN.

    Die Projektion maskierte `iban`, liess dieselbe Nummer aber ueber `name`
    passieren (Review PR #18, P1). Bestandszeilen erreicht nur ein Guard an
    der Grenze -- ein reiner Import-Fix haette sie weiter lecken lassen.
    """
    store.create_account("CAMT-Import DE89370400440532013000",
                         iban="DE89370400440532013000")
    row = store.transit_projection()[0]
    assert "DE89370400440532013000" not in str(row.values())
    assert row["name"] == "CAMT-Import " + "*" * 18 + "3000"


def test_transit_projection_reads_only_allowlisted_source_columns(store, monkeypatch):
    """The SQL boundary must not load sensitive or future columns into Python."""
    store.create_account("Girokonto", bank_name="Sparkasse", iban="DE89370400440532013000",
                         bic="COBADEFFXXX", account_type="girokonto", notes="Hauptkonto")
    store.create_account("Depot", bank_name="Broker", iban="DE001234", account_type="depot")
    with sqlite3.connect(store.db_path) as conn:
        conn.execute("ALTER TABLE bank_accounts ADD COLUMN future_sensitive_column TEXT")
        conn.execute("UPDATE bank_accounts SET future_sensitive_column = 'SECRET'")

    allowed_reads = {"name", "account_type", "balance", "balance_date", "iban"}
    actual_reads = []
    traced_statements = []
    original_connect = store.connect

    def monitored_connect():
        conn = original_connect()
        conn.set_trace_callback(traced_statements.append)

        def authorize(action, table, column, database, trigger):
            del database, trigger
            if action == sqlite3.SQLITE_READ and table == "bank_accounts":
                actual_reads.append(column)
                return sqlite3.SQLITE_OK if column in allowed_reads else sqlite3.SQLITE_DENY
            return sqlite3.SQLITE_OK

        conn.set_authorizer(authorize)
        return conn

    monkeypatch.setattr(store, "connect", monitored_connect)
    projection = store.transit_projection()

    selects = [" ".join(statement.split()) for statement in traced_statements
               if statement.lstrip().upper().startswith("SELECT")]
    assert selects == [
        "SELECT name, account_type, balance, balance_date, iban FROM bank_accounts ORDER BY name"
    ]
    assert set(actual_reads) == allowed_reads
    assert [row["name"] for row in projection] == ["Depot", "Girokonto"]
    assert all(tuple(row) == TRANSIT_FIELDS for row in projection)
    assert "SECRET" not in str(projection)


def _tables(db_path):
    with sqlite3.connect(db_path) as conn:
        return sorted(r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ))
