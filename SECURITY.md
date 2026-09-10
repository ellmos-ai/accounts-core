# Security Policy / Sicherheitsrichtlinie

## Supported Versions / Unterstützte Versionen

| Version | Supported / Unterstützt |
| ------- | ----------------------- |
| 0.1.x   | :white_check_mark:      |
| < 0.1   | :x:                     |

## Reporting a Vulnerability / Meldung von Sicherheitslücken

Do not open a public issue for a security vulnerability. Use GitHub Private Vulnerability
Reporting at:
[New repository security advisory](https://github.com/ellmos-ai/accounts-core/security/advisories/new)

Alternatively, contact the maintainers directly via:
- `security@open-bricks.org` (Umbrella organization)
- `security@ellmos.ai`
- `support@lukasgeiger.com`
- `lukas@open-bricks.org`

Include affected versions, impact, and minimal reproduction steps, but never send real
credentials, private bank details, or live database dumps.

Für Sicherheitslücken darf kein öffentliches Issue angelegt werden. Verwende
GitHub Private Vulnerability Reporting unter:
[New repository security advisory](https://github.com/ellmos-ai/accounts-core/security/advisories/new)

Alternativ können Sicherheitsberichte direkt an die folgenden Adressen gesendet werden:
- `security@open-bricks.org` (Dachorganisation)
- `security@ellmos.ai`
- `support@lukasgeiger.com`
- `lukas@open-bricks.org`

Nenne betroffene Versionen, Auswirkungen und minimale Reproduktionsschritte, aber keine echten
Zugangsdaten, vertraulichen Kontodaten oder Live-Datenbankauszüge.

## Response SLA & Triage / Reaktionszeiten und Triage-Zusagen

- **Response SLA:** We commit to acknowledging receipt of reports within **48 hours**.
- **Triage Commitment:** We commit to providing an initial triage and risk assessment within **5 business days**.
- **48-Stunden-Reaktions-SLA:** Eingangsbestätigung aller qualifizierten Berichte binnen **48 Stunden**.
- **5 Werktage verbindliche Triage-Zusage:** Erste Risikobewertung und Zeitplan für Behebung innerhalb von **5 Werktagen**.

## Scope & Architectural Guarantees / Geltungsbereich und Garantien

- **Local-First & Zero-Egress:** The core Python domain module operates entirely offline without telemetry or background network egress. All operations execute strictly on the local SQLite database file provided by the host application.
- **User-Mode Non-Elevation:** All routines, balance updates, and queries run unprivileged without elevated system permissions (RunAsInvoker).
- **Single Data Canon & Table Invariance:** `AccountStore` operates directly on the consumer's existing `bank_accounts` table. It creates no tables of its own and maintains no separate state.
- **Privacy-Safe Transit Allowlist:** The transit projection explicitly allowlists only `name`, `account_type`, `balance`, `balance_date`, and `iban_masked` (masking all but the last 4 characters). Sensitive banking attributes (full account number, BIC, bank name, holder name, internal notes) never leak through the transit boundary.
- **Fail-Closed Input Validation:** CAMT balance ingestion checks IBAN normalization and rejects malformed inputs without modifying unverified records.

## Operator boundary / Betreibergrenze

The module inspects and updates the database file passed to `AccountStore(db_path)`.
Run it only with trusted consumer database paths. Keep production database backups
and cryptographic keys outside the repository.

Das Modul greift ausschließlich auf den an `AccountStore(db_path)` übergebenen
Datenbankpfad zu. Es darf nur mit vertrauenswürdigen Konsumenten-Datenbanken verwendet
werden. Produktive Datensicherungen und kryptografische Schlüssel gehören nicht in das
Repository.
