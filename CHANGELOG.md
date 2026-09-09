# Changelog

## [0.1.1] - 2026-09-09

### Technical Hygiene & Domain Refinements (Pfad A)

- `AccountStore.transit_projection()` now selects only the five source columns needed for the
  public allowlisted result instead of loading every `bank_accounts` column through
  `list_accounts()`.
- CAMT warning messages now use genuine German umlauts (`unverändert`, `übersprungen`), with exact
  UTF-8 result strings covered by tests and documented in both README variants.
- Version synchronized to `0.1.1` across `pyproject.toml`, `ellmos-module.v2.json`,
  `src/accounts_core/__init__.py`, `llms.txt`, `CHANGELOG.md`, and README documentation.
- Standardized `pyproject.toml` with PEP 621 ecosystem URLs (`Homepage`, `Repository`,
  `Documentation`, `Issues`, `Changelog`, `Security`, `Parent Organization`, `Umbrella Ecosystem`),
  OS classifiers (`Windows`, `Linux`, `macOS`), and pytest configuration (`pythonpath = ["src", "."]`,
  `addopts = "-ra -v"`).
- Hardened `.gitignore` against multi-host synchronization conflicts (`*-conflict-*`,
  `*.sync-conflict-*`, `*.conflict`, `*-CONFLIT-*`, `*.sync-temp-*`), multi-agent locks (`LOCK`,
  `LOCK.*`, `*.lock`, `LOCK*.txt`, `LOCK.permissions.json`), test/coverage caches (`.pytest_cache/`,
  `.ruff_cache/`, `.coverage`, `coverage/`, `htmlcov/`, `wheelhouse/`, `.wheel-smoke/`), and
  temporary editor artifacts (`*.tmp`, `*.bak`, `*.swp`, `*~`, `*.log`).
- Created multi-OS GitHub Actions CI workflow (`.github/workflows/ci.yml`) covering `ubuntu-latest`,
  `windows-latest`, and `macos-latest` across Python 3.10–3.13 with concurrency control
  (`cancel-in-progress: true`), bytecode compilation gate (`compileall -q src tests`), ruff linting,
  and verbose pytest execution.
- Added bilingual security policy (`SECURITY.md`) with supported version matrix (`0.1.x`),
  binding 48-hour response SLA, 5-business-days triage commitment, official contacts
  (`security@open-bricks.org`, `security@ellmos.ai`, `support@lukasgeiger.com`, `lukas@open-bricks.org`),
  GitHub Security Advisories link, and Local-First / Zero-Egress scope definition.
- Added machine-readable AI context in `llms.txt` and synchronized Shields.io status badges across
  both `README.md` and `README_de.md`.
- Implemented automated contract test suite in `tests/test_metadata.py` covering metadata structure,
  PEP 621 URLs, pytest configuration, gitignore hygiene patterns, CI workflow integrity, security SLAs,
  badge parity, and version consistency.

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
