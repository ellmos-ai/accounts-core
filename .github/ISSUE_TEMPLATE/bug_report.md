---
name: Bug Report / Fehlerbericht
about: Report a bug or invariant violation / Einen Fehler oder eine Invarianten-Verletzung melden
title: "[Bug] "
labels: ["bug", "needs-triage"]
assignees: []
---

## Summary / Zusammenfassung

A clear and concise description of what the bug is.
Kurze, präzise Beschreibung des aufgetretenen Fehlers.

## Steps to Reproduce / Schritte zur Reproduktion

1. Database schema / Datenbankschema (`bank_accounts`):
2. Python call (`AccountStore` / `publish_transit_projection`):
3. Observed error or unexpected output / Beobachtetes Verhalten:

## Expected Behavior / Erwartetes Verhalten

What should have happened instead (e.g., which `INV-ACC-*` invariant applies)?
Was hätte stattdessen passieren sollen (z. B. welche Invariante `INV-ACC-*` ist betroffen)?

## Environment / Umgebung

- OS (Windows / Linux / macOS):
- Python version (`3.10`–`3.13`):
- `accounts-core` version (`python -c "import accounts_core; print(accounts_core.__version__)"`):

## Security & Privacy Reminder / Sicherheits- & Datenschutz-Hinweis

- Never paste real IBANs, BICs, bank account numbers, or private `*.db` dumps into public issues.
- Bitte niemals echte IBANs, BICs, Kontonummern oder private `*.db`-Auszüge in öffentliche Issues einfügen.
- For security vulnerabilities, follow [SECURITY.md](../../SECURITY.md) instead of opening a public issue.
- Sicherheitslücken bitte nicht öffentlich melden, sondern vertraulich gemäß [SECURITY.md](../../SECURITY.md).
