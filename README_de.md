# accounts-core

*[English](README.md)*

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

## Privacy (Modulgrenze)

Arbeitet nur auf dem übergebenen Datenbankpfad. Kein Netzwerk, keine Telemetrie, keine eigenen
Dateien. Bank-Stammdaten (Kontonummer, BIC, Inhabername) verlassen das Modul über die
Transit-Projektion nie — siehe Allowlist-Abschnitt oben.

## Projektstruktur

```
src/accounts_core/accounts.py    AccountStore, Transit-Projektion, CAMT-Salden-Persistenz
tests/test_accounts.py           Verhalten gegen die exakte BACH-bank_accounts-DDL
ellmos-module.v2.json            Modul-Manifest für den ellmos-Modulkatalog
```

## Entwicklung

```bash
python -m pytest -q
python -m ruff check src tests
```

## Lizenz

MIT. Kanonisches Repository: `ellmos-ai/accounts-core` (privat).
