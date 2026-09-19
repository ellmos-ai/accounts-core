# Changelog

## [0.1.4] - 2026-09-20

### Discoverability, Visual Architecture, 18-Point Quick Navigation & SBOM (Pfad B)

- **18-Point Bilingual Navigation Parity**: Restructured `README.md` and `README_de.md` into 18 synchronized sections with reciprocal HTML anchor parity (`<a id="..."></a>`), ensuring comprehensive bi-directional navigation.
- **Visual Architecture & Lifecycle Flow**: Validated dual Mermaid diagrams (`flowchart TD` architecture and `sequenceDiagram` lifecycle walkthrough with `autonumber`) adhering to strict quote escaping and zero-semicolon formatting.
- **Target Personas & SEO Discovery**: Codified 4 specific user personas (`[PERSONA-01]` to `[PERSONA-04]`) with high-intent search queries covering local-first FinTech, privacy-by-design architects, CAMT data integrators, and autonomous AI agents.
- **10-Dimension Comparative Matrix**: Documented full comparative analysis benchmarking `accounts-core` against Raw Ad-Hoc Scripts, Heavyweight ERPs (Odoo/Tryton), and Cloud SaaS APIs (Plaid/Tink) across 10 architectural criteria mapped to system invariants (`INV-ACC-01` to `INV-ACC-10`).
- **Governance & Runtime Invariants (10 Invariants)**: Expanded invariant index with `INV-ACC-09` (Unprivileged User-Mode Non-Elevation / RunAsInvoker) and `INV-ACC-10` (48h Security Response & 5-Day Triage SLA).
- **Level 1 SBOM & Software Inventory**: Enhanced `THIRD_PARTY_LICENSES.md` with Level 1 Software Bill of Materials, Invariant Cross-Reference Matrix table, and explicit RunAsInvoker certification.
- **Statutory Notice (§ 521 BGB)**: Codified legal disclaimer for non-commercial open-source distribution under German law.
- **GitHub Live Discoverability**: Expanded repository topics to 20/20 on GitHub and configured documentation homepage URL.
- **Automated Contract Test Suite Expansion**: Added contract tests in `tests/test_metadata.py` verifying quick navigation anchors, persona queries, comparative matrix dimensions, 10 invariants, and § 521 BGB notices.
- **Version Harmonization & Artifact Parity**: Bumped version to `0.1.4` across all manifests and documentation artifacts.

## [0.1.3] - 2026-09-12

### Technical Hygiene, CI Hardening & Stale Lifecycle (Pfad A)

- **CI Workflow Execution Guardrails**: Added `timeout-minutes: 15` to the test job in `.github/workflows/ci.yml` across Ubuntu, Windows, and macOS test matrices.
- **Automated Lifecycle Management**: Deployed canonical `.github/workflows/stale.yml` workflow for automated triage and closing of stale issues and pull requests.
- **Gitignore Multi-Host Defense**: Hardened `.gitignore` with multi-host conflict copy wildcards (`* (kopie)*`, `* (Kopie)*`, `* (copy)*`, `* (Copy)*`, `*conflicted copy*`, `*-WORKSTATION*`, `uv.lock`, `!package-lock.json`).
- **PEP 621 LLM-Ready Context Endpoint**: Added `"LLM Ready"` URL to `[project.urls]` in `pyproject.toml` pointing directly to raw `llms.txt`.
- **Ruff Linter Configuration**: Configured explicit `[tool.ruff.lint]` rule selection (`["E4", "E7", "E9", "F", "W", "B", "SIM", "C4", "RUF"]`) and harmonized `__all__` sorting in `src/accounts_core/__init__.py`.
- **Version Harmonization & Artifact Parity**: Bumped version to `0.1.3` across `pyproject.toml`, `ellmos-module.v2.json`, `src/accounts_core/__init__.py`, `llms.txt`, `TODO.md`, `README.md`, `README_de.md`, and `MARKETING-LOG.txt`.
- **Contract Test Suite Expansion**: Added automated contract tests in `tests/test_metadata.py` verifying CI timeout guardrail, stale lifecycle workflow existence, PEP 621 LLM-Ready URL, and gitignore conflict patterns.

## [0.1.2] - 2026-09-11

### Discoverability, Visual Architecture & Bilingual Parity (Pfad B)

- **Interactive Mermaid Flowchart & Sequence Diagram**: Added bilingual `flowchart TD` visual architecture diagrams and `sequenceDiagram` lifecycle walkthroughs with `autonumber` and strictly double-quoted node and edge labels satisfying `HOOK-BANNER-ASSET-01` and passing `_tools/lint_mermaid.py`.
- **Governance & System Invariants**: Formally codified 8 core system invariants (`INV-ACC-01` through `INV-ACC-08`) covering Zero Database Ownership, Strict 5-Field Allowlist, Masked IBAN Guarantee, Pure Local-First & Zero Egress, Immutable Source Isolation (`mode=ro`), Atomic Snapshot Publishing, Idempotent CAMT Balance Ingestion, and Deterministic Fail-Closed Error Handling.
- **Local Marketing & Integration Register**: Added `MARKETING-LOG.txt` detailing 4 primary user personas, discoverability keywords, catalog recommendations (Awesome-Python, Awesome-Privacy, LibHunt, PyPI), and 3 end-to-end integration blueprints.
- **Ecosystem & Sister Repositories Matrix**: Added cross-linking matrix mapping `accounts-core` to `bach`, `sqlite-transit-sync`, `assistant-core`, `open-ocean`, `report-forge`, and `open-bricks`.
- **Metadata & Discoverability Hardening**:
  - Bumped version to `0.1.2` across `pyproject.toml`, `ellmos-module.v2.json`, `src/accounts_core/__init__.py`, and `llms.txt`.
  - Added `"Marketing Log"` URL to `[project.urls]` in `pyproject.toml`.
  - Enriched keywords in `pyproject.toml` with `"financial-primitives"`, `"iban-validation"`, `"privacy-by-design"`, and `"zero-telemetry"`.
  - Synchronized `llms.txt` with timestamp `2026-09-11`, version `0.1.2`, and invariant index.

### Release Hygiene, Gate-Härtung & PEP 639 License Inventory

- **Final Gate Check Compliance (10/10 PASS)**: Brought the repository to full release readiness verified by the canonical `final_gate_check.py`.
- **Gitignore Hardening (Gate 1)**: Added mandatory `data/` ignore entry along with certificate, private key, token, credential, and multi-host synchronization exclusion patterns (`*.pem`, `*.key`, `*.pfx`, `*.p12`, `*.crt`, `*.cert`, `.npmrc`, `.pypirc`, `*token*`, `*secret*`, `credentials.json`, `secrets.json`, `id_rsa*`, `id_ed25519*`, `*-WORKSTATION-LG*`, `*-ASUS-GEI*`, `*-LAPTOP*`, `*.orig`, `*.rej`).
- **Standardized TODO.md (Gate 10)**: Created root `TODO.md` with structured `## STATUS` table and formalized future tasks (`TASK-AC-01`, `TASK-AC-02`, `TASK-AC-03`) adhering to end-user German umlaut conventions.
- **PEP 639 License Inventory**: Added `THIRD_PARTY_LICENSES.md` documenting the invariant of zero external runtime dependencies (100% Python Standard Library) and declared `license-files = ["LICENSE", "THIRD_PARTY_LICENSES.md"]` in `pyproject.toml`.
- **Contract Test Suite Expansion**: Added automated contract tests in `tests/test_metadata.py` verifying license inventory, zero dependencies, PEP 639 metadata, TODO status table, complete gitignore gate entries, and programmatic `final_gate_check.py` compliance.
- **Documentation & Badge Synchronization**: Synchronized test count badge and Last-checked timestamp (2026-09-11).

## [0.1.1] - 2026-09-09

### Technical Hygiene & Domain Refinements (Pfad A)

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
