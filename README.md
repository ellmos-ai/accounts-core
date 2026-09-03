# accounts-core

*[Deutsch](README_de.md)*

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

## Privacy (module boundary)

Works only on the database path it is given. No network, no telemetry, no files of its own.
Bank stammdaten (account number, BIC, holder name) never leave the module through the transit
projection -- see the allowlist section above.

## Project structure

```
src/accounts_core/accounts.py    AccountStore, transit projection, CAMT balance persistence
tests/test_accounts.py           behaviour against the exact BACH bank_accounts DDL
ellmos-module.v2.json            module manifest for the ellmos module catalog
```

## Development

```bash
python -m pytest -q
python -m ruff check src tests
```

## License

MIT. Canonical repository: `ellmos-ai/accounts-core` (private).
