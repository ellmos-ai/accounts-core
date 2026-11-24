---
name: accounts-core
version: "0.1.4"
description: "Neutral Python domain core for local-first bank account CRUD, idempotent CAMT balance persistence, and privacy-safe 5-field allowlist transit projection (masked IBANs, read-only SQLite snapshot publishing)."
license: MIT
homepage: https://github.com/ellmos-ai/accounts-core
requires:
  python: ">=3.10"
  dependencies: []
---

# accounts-core — Product Skill

## Purpose & Scope

`accounts-core` (`0.1.4`) is a pure Python standard-library domain module (`dependencies = []`, zero network egress, unprivileged `RunAsInvoker`) for:

1. **Bank Account CRUD (`AccountStore`):** Reading and writing the existing `bank_accounts` SQLite table in a consumer database without creating tables or running migrations (`INV-ACC-01`).
2. **Idempotent CAMT Balance Persistence (`persist_camt_balances`):** Upserting pre-parsed CAMT balance dictionaries (`[{"iban": ..., "balance": ..., "currency": ..., "date": ...}]`) matched by normalized IBAN (`INV-ACC-07`).
3. **Privacy-Safe Transit Projection (`to_transit_row`, `transit_projection`, `publish_transit_projection`):** Projecting strictly 5 allowlisted fields (`name`, `account_type`, `balance`, `balance_date`, `iban_masked`) while masking all IBANs to the last 4 characters and dropping all bank identifiers (`bic`, `bank_name`, `account_number`, `holder_name`, `notes`) (`INV-ACC-02`, `INV-ACC-03`).

### Explicit Non-Goals & Boundaries

- Does **not** parse raw CAMT XML files (`camt.052` / `camt.053`); consumers pass pre-parsed dictionaries.
- Does **not** create the SQLite database file or `bank_accounts` table; missing DB paths fail closed with `FileNotFoundError` (`INV-ACC-08`).
- Does **not** handle `credits` (Kredite) in Wave 1.
- Does **not** make any network requests, spawn background daemons, or require elevated privileges (`INV-ACC-04`, `INV-ACC-09`).

## Prerequisites & Safe Installation

- **Python:** `>= 3.10` (tested on `3.10`–`3.13` across Windows, Linux, macOS).
- **Runtime Dependencies:** None (100% Python standard library).

Install in an isolated virtual environment:

```bash
git clone https://github.com/ellmos-ai/accounts-core.git
cd accounts-core
python -m venv .venv
# Linux / macOS:
.venv/bin/pip install -e .
# Windows (PowerShell):
.\.venv\Scripts\pip.exe install -e .
```

Verify installation:

```bash
python -c "from accounts_core import AccountStore, publish_transit_projection, __version__; print(__version__)"
# Expected output: 0.1.4
```

## Public API & Usage Patterns

### 1. Account CRUD & CAMT Balance Persistence

```python
from accounts_core import AccountStore, default_db_path

# Optional environment lookup via BACH_DB (returns None if unset)
db_path = default_db_path() or "/path/to/finance.db"
store = AccountStore(db_path)

# Create, list, update, delete
account_id = store.create_account(
    "Girokonto",
    bank_name="Sparkasse",
    iban="DE89370400440532013000",
    bic="COBADEFFXXX",
    account_type="girokonto",
)
accounts = store.list_accounts()
store.update_account(account_id, "Hauptkonto", bank_name="Sparkasse")

# Idempotent CAMT balance upsert (returns list[str] German UTF-8 status lines)
lines = store.persist_camt_balances([
    {"iban": "DE89370400440532013000", "balance": 5420.50, "currency": "EUR", "date": "2026-09-15"}
])
# -> ["[OK] Konto DE89370400440532013000: Saldo 5420.50 EUR zum 2026-09-15 aktualisiert."]
```

### 2. In-Memory Allowlist Transit Projection

```python
projection = store.transit_projection()
# Returns list[dict] with ONLY TRANSIT_FIELDS:
# ('name', 'account_type', 'balance', 'balance_date', 'iban_masked')
# e.g. [{'name': 'Hauptkonto', 'account_type': 'girokonto', 'balance': 5420.5,
#        'balance_date': '2026-09-15', 'iban_masked': '******************3000'}]
```

Also masks IBANs embedded inside free-text `name` values via `mask_ibans_in_text()` / `mask_iban()`.

### 3. Atomic Read-Only Snapshot Publishing (`publish_transit_projection`)

```python
from accounts_core import publish_transit_projection

report = publish_transit_projection(
    "/path/to/source/finance.db",          # opened strictly with mode=ro + PRAGMA query_only = ON
    "/path/to/transit/accounts.sqlite",    # atomic temp write + os.replace()
    "/path/to/state/checkpoint.json",      # stores {"checkpoint": int, "salt": hex}
    publisher_instance="bach-primary",     # matches ^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$
)
# Returns dict:
# {'status': 'published-read-only-projection',
#  'contract_id': 'org.ellmos.accounts.balance-projection',
#  'contract_version': '1.0.0', 'source_checkpoint': 1, 'record_count': 1,
#  'complete_snapshot': True, ...}
```

## Authority, Side Effects & Fail-Closed Error Modes

- **Source Isolation (`INV-ACC-05`):** `publish_transit_projection` opens `source_db_path` via URI `?mode=ro` and `PRAGMA query_only = ON`, preserving literal `#`, `%`, spaces, and Unicode in filenames.
- **Distinct Paths (`INV-ACC-05`):** `source_db_path`, `output_path`, and `checkpoint_path` must resolve to three distinct paths (`ValueError` otherwise).
- **Missing Files (`INV-ACC-08`):** Non-existent database or missing parent directories for output/checkpoint raise `FileNotFoundError` before creating 0-byte files.
- **Invalid Contracts (`INV-ACC-08`):** Invalid `publisher_instance`, invalid `salt` (must be 32–128 lowercase hex chars), naive `now` datetime, or malformed checkpoint JSON raise `ValueError`.
- **Atomic Output (`INV-ACC-06`):** Snapshots pass `PRAGMA quick_check` before `os.replace()`.

## Verification & Quality Gates

```bash
python -m pytest -ra -v
python -m ruff check src tests
python -m compileall -q src tests
```

## Related Documentation

- [README.md](README.md) / [README_de.md](README_de.md)
- [llms.txt](llms.txt) / [llm.txt](llm.txt)
- [SECURITY.md](SECURITY.md) / [THIRD_PARTY_LICENSES.txt](THIRD_PARTY_LICENSES.txt)
