# Changelog

## Unreleased

- Added the application-owned `accounts-core` publisher for the versioned
  `org.ellmos.accounts.balance-projection` read-only SQLite contract. It opens
  the BACH source database read-only, writes a separate complete snapshot
  atomically, emits only the five existing transit allowlist fields, and uses
  the source id only as salted hash input.
- `AccountStore.transit_projection()` now selects only the five source columns needed for the
  public allowlisted result instead of loading every `bank_accounts` column through
  `list_accounts()`.
- CAMT warning messages now use genuine German umlauts (`unverändert`, `übersprungen`), with exact
  UTF-8 result strings covered by tests and documented in both README variants.

## 0.1.0 - 2026-09-03

Wave 1 of the account domain cut (decision D-20260903-003 = A, analysis
`KONTEN-DOMAENE-OCEAN-ANALYSE_2026-09-03.md`). Same pattern as `assistant-core` wave 1.

- `AccountStore(db_path)`: `list_accounts`, `create_account`, `update_account`, `delete_account`
  -- the exact SQL BACH's `/api/financial/bank-accounts` endpoints used, behind one API.
- `AccountStore.persist_camt_balances(balances)`: identical UPSERT-by-normalized-IBAN logic to
  BACH's `hub/steuer.py::_persist_camt_balances`. Takes already-parsed balance dicts; the CAMT
  XML format itself stays BACH's concern.
- `AccountStore.transit_projection()` / `to_transit_row()`: privacy-safe read-only projection.
  Allowlist of exactly `name`, `account_type`, `balance`, `balance_date`, `iban_masked` -- built
  by naming the allowed fields, never by removing keys, so a new `bank_accounts` column can never
  leak through by accident. No account number, no BIC, IBAN masked to its last 4 characters.
- `default_db_path()` reads the consumer's `BACH_DB` environment seam, same as `assistant-core`.
- `credits` (Kredite) intentionally out of scope for wave 1 -- related but separate domain.
- 15 behavioural tests against the exact BACH `bank_accounts` DDL, including the "module creates
  no tables" guard and a dedicated allowlist regression test (unknown source column must not
  appear in the projection).
