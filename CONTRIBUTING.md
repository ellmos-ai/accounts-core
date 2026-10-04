# Contributing to accounts-core

[English](#english) | [Deutsch](#deutsch)

---

<a id="english"></a>
## English

Thank you for your interest in contributing to **accounts-core**!

### Architectural Principles & Governance Invariants

`accounts-core` is an unprivileged domain core for bank account CRUD, CAMT balance import, and privacy-safe read-only transit projections. All contributions must respect all 10 foundational invariants:

1. **Zero Database Ownership (`INV-ACC-01`)**: The core defines domain logic and migrations, but never owns consumer databases or creates unapproved tables.
2. **Strict Allowlist Transit Projection (`INV-ACC-02`)**: Transit projections only emit explicitly allowlisted fields (`name`, `account_type`, `balance`, `balance_date`, `iban_masked`), eliminating schema leakage.
3. **Masked IBAN Guarantee (`INV-ACC-03`)**: Raw bank identifiers, BIC, account numbers, and bank names never escape through the transit projection; IBAN is strictly masked (`****1234`).
4. **100% Local-First & Zero-Egress (`INV-ACC-04`)**: All computation is executed purely locally in user space without external network calls, sockets, telemetry, or cloud services.
5. **Immutable Source Isolation (`INV-ACC-05`)**: Source databases are opened with explicit `mode=ro` during transit publishing; source, destination, and checkpoint paths remain distinct.
6. **Atomic Snapshot Publishing (`INV-ACC-06`)**: Published transit projections are written to temporary staging files and committed via atomic filesystem rename to prevent torn reads.
7. **Idempotent CAMT Balance Ingestion (`INV-ACC-07`)**: CAMT balance ingestion matches accounts strictly by normalized IBAN and reports deterministic status feedback.
8. **Deterministic Fail-Closed Error Handling (`INV-ACC-08`)**: Unexpected inputs or missing files raise typed standard exceptions without partial or dirty state writes.
9. **RunAsInvoker User-Mode Non-Elevation (`INV-ACC-09`)**: Code must run purely in unprivileged user space. Never require root, sudo, administrator rights, or UAC elevation.
10. **48h Security Response SLA (`INV-ACC-10`)**: Binding 48h response and 5-day triage SLA backed by contract test suite and responsible disclosure policies.

### Version Freeze & Release Governance

- **Version Freeze Policy (`T-20260920-167562623`)**: Version `0.1.4` is strictly frozen. Zero arbitrary version bumps. All improvements, CI hardening, and contract expansions are documented under `## [Unreleased]` in `CHANGELOG.md`.

### Development & Quality Gates

- **Plan D Architecture**: Development, git operations, and tests occur strictly in the local git repository clone. OneDrive mirrors are derived read-only surfaces.
- **Python Version Support**: Compatible with Python 3.10 through 3.13. Zero external runtime dependencies (`dependencies = []`).
- **Pre-commit Quality Gates**:
  - Bytecode compilation: `python -m compileall -q src tests`
  - Linting: `ruff check src tests`
  - Automated test suite: `pytest -ra -v` (100% green required)
  - Git whitespace hygiene: `git diff --check`
- **Security Vulnerabilities**: Please do not report security vulnerabilities publicly. Follow our [SECURITY.md](SECURITY.md) guidelines for responsible disclosure (48h response SLA) via `security@ellmos.ai`, `security@open-bricks.org`, `support@lukasgeiger.com`, or `lukas@open-bricks.org`.

### Statutory Notice (§ 521 BGB)

Provided free of charge under the MIT License as open-source software. Under German statutory law (§ 521 BGB), liability in the case of gratuitous provision is limited to intent and gross negligence.

---

<a id="deutsch"></a>
## Deutsch

Vielen Dank für Ihr Interesse an einer Mitarbeit an **accounts-core**!

### Architektur-Prinzipien & Governance-Invarianten

`accounts-core` ist der neutrale Fachkern für Bankkonten-CRUD, CAMT-Saldenimport und datenschutzsichere Transit-Projektionen. Alle Beiträge müssen alle 10 grundlegenden Invarianten einhalten:

1. **Kein Datenbank-Eigentum (`INV-ACC-01`)**: Der Kern stellt Domänenlogik und Migrationen bereit, übernimmt aber kein Eigentum an Konsumenten-Datenbanken und legt keine unbefugten Tabellen an.
2. **Strikte Allowlist-Transit-Projektion (`INV-ACC-02`)**: Transit-Projektionen geben ausschließlich explizit erlaubte Felder aus (`name`, `account_type`, `balance`, `balance_date`, `iban_masked`), wodurch Schemalecks ausgeschlossen werden.
3. **Maskierte IBAN-Garantie (`INV-ACC-03`)**: Rohe Bankkennungen, BICs, Kontonummern oder Banknamen werden niemals über die Transit-Projektion exponiert; IBANs werden strikt maskiert (`****1234`).
4. **100% Local-First & Zero-Egress (`INV-ACC-04`)**: Sämtliche Verarbeitung erfolgt lokal im Benutzerkontext ohne externe Netzwerkaufrufe, Sockets, Telemetrie oder Cloud-Dienste.
5. **Unveränderliche Quell-Isolation (`INV-ACC-05`)**: Quelldatenbanken werden beim Publishing mit `mode=ro` geöffnet; Quell-, Ziel- und Checkpoint-Pfade bleiben strikt getrennt.
6. **Atomares Snapshot-Publishing (`INV-ACC-06`)**: Veröffentlichte Transit-Projektionen werden temporär bereitgestellt und atomar umbenannt, um unvollständige Lesevorgänge zu verhindern.
7. **Idempotente CAMT-Saldenübernahme (`INV-ACC-07`)**: CAMT-Salden werden anhand normalisierter IBANs zugeordnet und liefern deterministisches Rückmeldungs-Feedback.
8. **Deterministisches Fail-Closed-Verhalten (`INV-ACC-08`)**: Unerwartete Eingaben oder fehlende Pfade werfen typisierte Standardausnahmen ohne inkonsistente Zwischenstände.
9. **RunAsInvoker User-Mode (`INV-ACC-09`)**: Code wird ausschließlich ohne administrative Rechte ausgeführt. Keine Root-, Sudo- oder UAC-Elevation erforderlich.
10. **48h Sicherheitsreaktions-SLA (`INV-ACC-10`)**: Verbindliche 48-Stunden-Erstantwort und 5-Tage-Triage gemäß Sicherheitsrichtlinie und Vertragstest-Prüfung.

### Versions-Freeze & Release-Governance

- **Version-Freeze-Regel (`T-20260920-167562623`)**: Version `0.1.4` ist strikt eingefroren. Keine Version-Bumps. Alle Verbesserungen, CI-Härtungen und Vertragstests werden unter `## [Unreleased]` in `CHANGELOG.md` gepflegt.

### Richtlinien für Entwickler

- **Plan D Architektur**: Entwicklung und Tests erfolgen ausschließlich im lokalen Git-Repository. OneDrive-Spiegel dienen als abgeleitete Leseansichten.
- **Python-Unterstützung**: Python 3.10 bis 3.13. Null externe Laufzeit-Abhängigkeiten (`dependencies = []`).
- **Qualitäts-Tore vor Commits**:
  - Bytecode-Prüfung: `python -m compileall -q src tests`
  - Linter: `ruff check src tests`
  - Testsuite: `pytest -ra -v` (100% grün erforderlich)
  - Whitespace-Prüfung: `git diff --check`
- **Sicherheitsmeldungen**: Sicherheitslücken bitte nicht öffentlich melden, sondern gemäß [SECURITY.md](SECURITY.md) vertraulich einreichen (48h Reaktions-SLA) an `security@ellmos.ai`, `security@open-bricks.org`, `support@lukasgeiger.com` oder `lukas@open-bricks.org`.

### Gesetzlicher Haftungsausschluss (§ 521 BGB)

Die Bereitstellung erfolgt unentgeltlich als Open-Source-Software unter den Bedingungen der MIT-Lizenz. Gemäß § 521 BGB ist die Haftung bei unentgeltlicher Überlassung auf Vorsatz und grobe Fahrlässigkeit beschränkt.
