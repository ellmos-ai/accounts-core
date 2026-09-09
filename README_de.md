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

Neutraler Fachkern für die Konten-/Kontostand-Domäne. Welle 1 liefert Bankkonten-CRUD,
CAMT-Salden-Import und eine **privacy-sichere, read-only Transit-Projektion** für andere
Konsumenten (z. B. OCEAN).

Aus [BACH](https://github.com/ellmos-ai/bach) extrahiert, damit BACH und OCEAN dieselben
Kontodaten über eine Implementierung lesen, statt dass BACH eine zweite, auseinanderdriftende
Kopie hält (Entscheidung D-20260903-003 = A, Analyse
`KONTEN-DOMAENE-OCEAN-ANALYSE_2026-09-03.md`). Gleiches Welle-1-Muster wie
[assistant-core](https://github.com/ellmos-ai/assistant-core) (D-20260830-002).

## Vertrag

- **Ein Datenkanon.** `AccountStore` bekommt den SQLite-Pfad des Konsumenten (BACH: `bach.db`)
  und arbeitet auf der vorhandenen Tabelle `bank_accounts`. Das Modul legt keine Tabellen an und
  hält keine eigenen Daten.
- **Kein UI-Toolkit, kein HTTP, kein XML-Parsing.** Konsumenten verdrahten Endpunkte gegen diese
  API und übergeben `persist_camt_balances` bereits geparste Salden-Dicts (die Form, die BACHs
  `CamtParser.parse_balances()` liefert) — das CAMT-Dateiformat bleibt eine BACH-seitige Sache.
- **Verhalten identisch zu BACH.** Jede SQL-Anweisung ist die, die BACH vor der Extraktion
  ausführte; nur die Aufrufstelle ist gewandert.
- **`credits` (Kredite) ist NICHT Teil von Welle 1.** Laut Analyse eine verwandte, aber eigene
  Domäne; bei Bedarf in einer späteren Welle ergänzen.

## Privacy: die Transit-Projektion ist eine Allowlist, keine Denylist

`AccountStore.transit_projection()` liefert **ausschließlich** `name`, `account_type`, `balance`,
`balance_date` und `iban_masked` (letzte 4 Zeichen, Rest durch `*` ersetzt). Keine Kontonummer,
kein BIC, kein Bankname, kein Inhabername, keine Notizen — und entscheidend: **kein Feld, das
`bank_accounts` später hinzugefügt wird, kann versehentlich durchsickern**: `to_transit_row()`
baut das Ergebnis, indem es die fünf erlaubten Felder ausdrücklich benennt, nie indem es Schlüssel
aus der Quellzeile entfernt. Eine Denylist vergisst die nächste Spalte, die jemand hinzufügt; eine
Allowlist kann das nicht. Siehe der Regressionstest
`test_to_transit_row_drops_bank_identifiers_and_unknown_columns`.

## Installation

```bash
pip install -e .            # in der Umgebung des Konsumenten
pip install -e ".[dev]"     # zusätzlich pytest und ruff
```

Python 3.10+, keine Laufzeit-Abhängigkeiten.

## Nutzung

```python
from accounts_core import AccountStore

store = AccountStore("/pfad/zu/bach.db")          # oder default_db_path() -> BACH_DB-Env
account_id = store.create_account("Girokonto", bank_name="Sparkasse", iban="DE89...", bic="...")
store.list_accounts()
store.update_account(account_id, "Neuer Name", bank_name="Sparkasse")
store.delete_account(account_id)

# CAMT-Import: bereits geparste Salden übergeben (Form von BACHs CamtParser.parse_balances())
store.persist_camt_balances([{"iban": "DE89...", "balance": 1234.56, "currency": "EUR", "date": "2026-09-01"}])

# Read-only Projektion für andere Konsumenten (OCEAN via sqlite-transit-sync, Welle 3)
store.transit_projection()
# -> [{"name": "Girokonto", "account_type": "girokonto", "balance": 1234.56,
#      "balance_date": "2026-09-01", "iban_masked": "*"*18 + "3000"}]
```

`persist_camt_balances()` liefert deutsche UTF-8-Ergebnismeldungen mit echten Umlauten, etwa
`unverändert` und `übersprungen`.

## Privacy (Modulgrenze)

Arbeitet nur auf dem übergebenen Datenbankpfad. Kein Netzwerk, keine Telemetrie, keine eigenen
Dateien. Bank-Stammdaten (Kontonummer, BIC, Inhabername) verlassen das Modul über die
Transit-Projektion nie — siehe Allowlist-Abschnitt oben.

## Projektstruktur

```
src/accounts_core/accounts.py    AccountStore, Transit-Projektion, CAMT-Salden-Persistenz
src/accounts_core/__init__.py    Öffentliche API-Exporte und Modulversion
tests/test_accounts.py           Verhalten gegen die exakte BACH-bank_accounts-DDL
tests/test_metadata.py           Vertragstests für Metadaten, Security SLAs, CI und Parität
SECURITY.md                      Zweisprachige Sicherheitsrichtlinie mit 48h-SLA & 5-Tage-Triage
llms.txt                         Maschinenlesbares LLM-Kontextdokument
ellmos-module.v2.json            Modul-Manifest für den ellmos-Modulkatalog
```

## Entwicklung

```bash
pytest -ra -v
python -m ruff check src tests
python -m compileall -q src tests
```

## Lizenz

MIT. Kanonisches Repository: `ellmos-ai/accounts-core` (privat).
