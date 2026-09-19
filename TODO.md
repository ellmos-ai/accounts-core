# TODO.md — Active work

**Version:** 0.1.4
**Updated:** 2026-09-20
**Reason:** Discoverability, visual architecture, 18-point bilingual quick navigation parity, target personas, 10-dimension comparative matrix, dual Mermaid diagrams, Level 1 SBOM, and statutory notice (§ 521 BGB)
**Purpose:** Track only work that remains open.

## STATUS

| Category | Status | Evidence / next gate |
|---|---|---|
| Core Account Store | DONE | CRUD operations, normalized IBAN lookups, ordering semantics verified by 29 automated tests (100% green). |
| CAMT Balance Import | DONE | Pre-parsed CAMT balance dictionary ingestion, non-destructive updates, balance date tracking verified. |
| Transit Projection Allowlist | DONE | Strict allowlist projection (`name`, `account_type`, `balance`, `balance_date`, `iban_masked`) with zero data leakage. |
| Path Neutrality & Hygiene | DONE | Neutral environments, standard `.gitignore` patterns, zero personal paths, zero secrets. |
| AI Discoverability & Metadata | DONE | Machine-readable `llms.txt`, PEP 621 classifiers, PEP 639 license inventory, schema v2 metadata parity. |
| Ecosystem Integration | DONE | Registered in `.MODULES/.RUNTIME/accounts-core`, Plan-D pointer configured, shared between BACH and OCEAN. |
| Public Release Gate | USER | MIT License selected; explicit public visibility approval pending from user. |

## Formalized next tasks

- [ ] **TASK-AC-01: CAMT.054 V2 Detailposten-Erweiterung** (`effort=medium`, `scope=camt`, priority `normal`).
  - **Ziel:** Unterstützung für optionale Einzeltransaktions-Splits aus CAMT.054 Avise-Meldungen bei Bedarf künftiger Konsumenten.
  - **Definition of Done:** Optionales Schema für Buchungszeilen definiert; abwärtskompatible Erweiterung ohne Bruch der bestehenden Kontensalden-Schnittstelle.

- [ ] **TASK-AC-02: Erweiterte Währungs- und Valuta-Prüfung** (`effort=low`, `scope=validation`, priority `normal`).
  - **Ziel:** ISO 4217 Währungscode-Validierung und formale Valuta-Prüfungen vor dem Schreiben in den Primärspeicher.
  - **Definition of Done:** Reine Standardbibliothek-Validierung (`re`, `datetime`); automatisierte Tests in `tests/test_accounts.py`.

- [x] **TASK-AC-03: Release-Hygiene, Lizenzinventar & Gate-Bereitschaft (v0.1.1)** (`effort=low`, `scope=hygiene`, priority `high`).
  - **Ergebnis:** Standard-`TODO.md` mit `## STATUS`-Tabelle etabliert, `THIRD_PARTY_LICENSES.md` angelegt, `.gitignore` um `data/` und Sicherheitsmuster gehärtet, `final_gate_check.py` auf 10/10 PASS gebracht.

---
<!-- REMEMBER: ENDUSERTEXTE BEKOMMEN ECHTE UMLAUTE Ü Ö Ä ß -->
