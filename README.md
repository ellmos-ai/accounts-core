# accounts-core

[English](README.md) | [Deutsch](README_de.md)

<p align="center">
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/version-0.1.1-blue.svg" alt="Version 0.1.1"></a>
  <a href="https://github.com/ellmos-ai/accounts-core/actions/workflows/ci.yml"><img src="https://github.com/ellmos-ai/accounts-core/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI"></a>
  <a href="tests/"><img src="https://img.shields.io/badge/tests-26%20passed%20%7C%20100%25%20green-brightgreen.svg" alt="Tests"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg" alt="Python"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Platform"></a>
  <a href="SECURITY.md"><img src="https://img.shields.io/badge/privacy-100%25%20Local--First%20%7C%20Zero--Egress-brightgreen.svg" alt="Local-First Zero-Egress"></a>
  <a href="SECURITY.md"><img src="https://img.shields.io/badge/security%20SLA-48h%20response%20%7C%205d%20triage-blue.svg" alt="Security SLA"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/badge/code%20style-ruff-000000.svg" alt="Code style: ruff"></a>
  <a href="https://github.com/ellmos-ai"><img src="https://img.shields.io/badge/ecosystem-ellmos--ai-informational.svg" alt="Ecosystem ellmos-ai"></a>
  <a href="https://github.com/open-bricks"><img src="https://img.shields.io/badge/umbrella-open--bricks-informational.svg" alt="Umbrella open-bricks"></a>
  <a href="llms.txt"><img src="https://img.shields.io/badge/LLM-llms.txt-blueviolet.svg" alt="LLM Context"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License: MIT"></a>
</p>

Neutral domain core for the account/bank-balance domain. Wave 1 ships bank account CRUD,
CAMT balance import, and a **privacy-safe read-only transit projection** for other consumers
(e.g. OCEAN).

Extracted from [BACH](https://github.com/ellmos-ai/bach) so that BACH and OCEAN read the same
account data through one implementation instead of BACH owning a second, drifting copy
(decision D-20260903-003 = A, analysis `KONTEN-DOMAENE-OCEAN-ANALYSE_2026-09-03.md`). Same wave-1
pattern as [assistant-core](https://github.com/ellmos-ai/assistant-core) (D-20260830-002).

## Contract

- **One data canon.** `AccountStore` is handed the consumer's SQLite path (BACH: `bach.db`) and
  works on the existing `bank_accounts` table. It creates no tables and keeps no data of its own.
- **No UI toolkit, no HTTP, no XML parsing.** Consumers wire endpoints against this API and hand
  `persist_camt_balances` already-parsed balance dicts (the shape BACH's `CamtParser.parse_balances()`
  returns) -- the CAMT file format stays a BACH-side concern.
- **Behaviour identical to BACH.** Every SQL statement is the one BACH ran before the extraction;
  only the call site moved.
- **`credits` (Kredite) is out of wave 1.** A related but separate domain per the analysis; add it
  in a later wave if a consumer needs it.

## Privacy: the transit projection is an allowlist, not a denylist

`AccountStore.transit_projection()` returns **only** `name`, `account_type`, `balance`,
`balance_date`, and `iban_masked` (last 4 characters, the rest replaced by `*`). No account
number, no BIC, no bank name, no holder name, no notes -- and, critically, **no field that gets
added to `bank_accounts` later leaks through by accident**: `to_transit_row()` builds the result
by naming the five allowed fields explicitly, never by removing keys from the source row. A
denylist forgets the next column someone adds; an allowlist cannot. See
`test_to_transit_row_drops_bank_identifiers_and_unknown_columns` for the regression test.

## Install

```bash
pip install -e .            # in the consumer's environment
pip install -e ".[dev]"     # plus pytest and ruff
```

Python 3.10+, no runtime dependencies.

## Usage

```python
from accounts_core import AccountStore

store = AccountStore("/path/to/bach.db")          # or default_db_path() -> BACH_DB env
account_id = store.create_account("Girokonto", bank_name="Sparkasse", iban="DE89...", bic="...")
store.list_accounts()
store.update_account(account_id, "Neuer Name", bank_name="Sparkasse")
store.delete_account(account_id)

# CAMT import: hand it already-parsed balances (BACH's CamtParser.parse_balances() shape)
store.persist_camt_balances([{"iban": "DE89...", "balance": 1234.56, "currency": "EUR", "date": "2026-09-01"}])

# Read-only projection for other consumers (OCEAN via sqlite-transit-sync, wave 3)
store.transit_projection()
# -> [{"name": "Girokonto", "account_type": "girokonto", "balance": 1234.56,
#      "balance_date": "2026-09-01", "iban_masked": "*"*18 + "3000"}]
```

`persist_camt_balances()` returns UTF-8 German result messages with genuine umlauts, such as
`unverändert` and `übersprungen`.

## Privacy (module boundary)

Works only on the database path it is given. No network, no telemetry, no files of its own.
Bank stammdaten (account number, BIC, holder name) never leave the module through the transit
projection -- see the allowlist section above.

## Project structure

```
src/accounts_core/accounts.py    AccountStore, transit projection, CAMT balance persistence
src/accounts_core/__init__.py    Public module exports and package version
tests/test_accounts.py           behaviour against the exact BACH bank_accounts DDL
tests/test_metadata.py           contract tests for metadata, security SLAs, CI and parity
SECURITY.md                      bilingual security policy with 48h response SLA & 5d triage
llms.txt                         machine-readable LLM context document
ellmos-module.v2.json            module manifest for the ellmos module catalog
```

## Development

```bash
pytest -ra -v
python -m ruff check src tests
python -m compileall -q src tests
```

## License

MIT. Canonical repository: `ellmos-ai/accounts-core` (private).
