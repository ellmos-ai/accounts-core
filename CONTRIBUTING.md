# Contributing to accounts-core

[English](#english) | [Deutsch](#deutsch)

---

<a id="english"></a>
## English

Thank you for your interest in contributing to **accounts-core**!

### Architectural Principles & Quality Invariants

`accounts-core` is a neutral domain core for bank account CRUD, CAMT balance import, and privacy-safe read-only transit projections. All contributions must respect our foundational invariants:

1. **Zero Database Ownership (`INV-ACC-01`)**: The core defines domain logic and migrations, but never owns consumer databases.
2. **Strict Allowlist Transit Projection (`INV-ACC-02`, `INV-ACC-03`)**: Transit projections only emit allowed fields (`name`, `type`, `balance`, `date`, `iban_masked`) with IBANs masked (`****1234`). Never expose raw bank credentials, BIC, or internal IDs.
3. **100% Local-First & Zero-Egress (`INV-ACC-04`)**: All computation is executed locally in user space without external network calls or cloud dependencies.
4. **RunAsInvoker Non-Elevation (`INV-ACC-09`)**: Code must run purely in unprivileged user space. Never require root, sudo, or UAC elevation.
5. **Deterministic Fail-Closed Error Handling (`INV-ACC-08`)**: Unexpected inputs must raise typed standard exceptions without partial or dirty state writes.

### Development Guidelines

- **Plan D Architecture**: Development, git operations, and tests occur strictly in the local git repository clone (`C:\_Local_DEV\repos\accounts-core`). OneDrive mirrors are derived read surfaces.
- **Python Version Support**: Compatible with Python 3.10 through 3.13. Zero external runtime dependencies (`dependencies = []`).
- **Pre-commit Quality Gates**:
  - Bytecode compilation: `python -m compileall -q src tests`
  - Linting: `ruff check src tests`
  - Automated test suite: `pytest -ra -v` (100% green required)
- **Security Vulnerabilities**: Please do not report security vulnerabilities publicly. Follow our [SECURITY.md](SECURITY.md) guidelines for responsible disclosure (48h response SLA).

---

<a id="deutsch"></a>
## Deutsch

Vielen Dank für Ihr Interesse an einer Mitarbeit an **accounts-core**!

### Architektur-Prinzipien & Qualitäts-Invarianten

`accounts-core` ist der neutrale Domänenkern für Bankkonten-CRUD, CAMT-Saldenimport und datenschutzsichere Transit-Projektionen. Alle Beiträge müssen unsere grundlegenden Invarianten einhalten:

1. **Kein Datenbank-Eigentum (`INV-ACC-01`)**: Der Kern stellt Domänenlogik und Migrationen bereit, übernimmt aber kein Eigentum an Konsumenten-Datenbanken.
2. **Strikte Allowlist-Transit-Projektion (`INV-ACC-02`, `INV-ACC-03`)**: Transit-Projektionen geben nur erlaubte Felder aus (`name`, `type`, `balance`, `date`, `iban_masked`) mit maskierter IBAN (`****1234`). Rohe Bankkennungen, BICs oder interne IDs werden niemals exponiert.
3. **100% Local-First & Zero-Egress (`INV-ACC-04`)**: Sämtliche Verarbeitung erfolgt lokal im Benutzerkontext ohne externe Netzwerkaufrufe oder Cloud-Dienste.
4. **RunAsInvoker User-Mode (`INV-ACC-09`)**: Code wird ausschließlich ohne administrative Rechte ausgeführt. Keine Root-, Sudo- oder UAC-Elevation erforderlich.
5. **Deterministisches Fail-Closed-Verhalten (`INV-ACC-08`)**: Unerwartete Eingaben werfen typisierte Standardausnahmen ohne inkonsistente Zwischenstände.

### Richtlinien für Entwickler

- **Plan D Architektur**: Entwicklung und Tests erfolgen ausschließlich im lokalen Git-Repository (`C:\_Local_DEV\repos\accounts-core`).
- **Python-Unterstützung**: Python 3.10 bis 3.13. Null externe Laufzeit-Abhängigkeiten (`dependencies = []`).
- **Qualitäts-Tore vor Commits**:
  - Bytecode-Prüfung: `python -m compileall -q src tests`
  - Linter: `ruff check src tests`
  - Testsuite: `pytest -ra -v` (100% grün erforderlich)
- **Sicherheitsmeldungen**: Sicherheitslücken bitte nicht öffentlich melden, sondern gemäß [SECURITY.md](SECURITY.md) vertraulich einreichen (48h Reaktions-SLA).
