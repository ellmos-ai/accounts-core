# Third-Party Licenses & Software Inventory

**Project:** `accounts-core`
**License:** [MIT License](LICENSE)
**Audit Date:** 2026-09-29 (v0.1.4)
**Status:** Invariant Confirmed — Zero External Runtime Dependencies (Level 1 SBOM)
**Notice & Attribution:** [NOTICE](NOTICE)
**Plain-Text Companion:** [THIRD_PARTY_LICENSES.txt](THIRD_PARTY_LICENSES.txt)
**Privilege Model:** `RunAsInvoker` (Strict User-Mode Non-Elevation)

---

## Runtime Architecture & Level 1 SBOM

`accounts-core` is engineered as a zero-egress, local-first domain core for bank account operations, CAMT balance ingestion, and privacy-safe transit projections. To preserve maximum operational reliability, deterministic multi-OS execution, and eliminate supply-chain attack vectors, `accounts-core` enforces a strict **Zero-Runtime-Dependency** invariant.

### Runtime Dependencies (Level 1 SBOM)

| Package | Version Spec | License | Scope | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| *(None)* | `N/A` | `N/A` | `runtime` | 100% pure Python standard library (`sqlite3`, `pathlib`, `typing`, `dataclasses`, `logging`, `os`, `sys`, `re`, `datetime`) under PSF License 2.0 |

All core subsystems—including `AccountStore` CRUD methods, CAMT balance ingestion (`persist_camt_balances`), and the allowlist-based transit projection (`publish_transit_projection` / `transit_projection`)—run entirely on the Python Standard Library without third-party wheels or runtime packages.

---

## Invariant Cross-Reference Matrix

Every architectural invariant in `accounts-core` is directly backed by formal testing and license guarantees:

| Invariant ID | Name | Architectural Scope | Compliance & License Guarantee |
| :--- | :--- | :--- | :--- |
| `INV-ACC-01` | Zero Database Ownership | SQLite Schema Isolation | Standard library `sqlite3` only; operates strictly within consumer database schema without creating rogue tables. |
| `INV-ACC-02` | Strict Allowlist Projection | Data Minimization | Explicit 5-field projection tuple (`name`, `account_type`, `balance`, `balance_date`, `iban_masked`); eliminates schema leakage. |
| `INV-ACC-03` | Masked IBAN Guarantee | Privacy by Design | Unmasked IBAN strings and bank identifiers (BIC, account number) never leave core boundary; masked to last 4 characters. |
| `INV-ACC-04` | Pure Local-First & Zero Egress | Network Perimeter | Zero network egress, zero sockets, 100% offline stdlib execution; verified by contract test suite. |
| `INV-ACC-05` | Immutable Source Isolation | Concurrency & Safety | Primary SQLite database is opened with explicit `mode=ro` during transit publishing; prevents write lock contention. |
| `INV-ACC-06` | Atomic Snapshot Publishing | Fault Tolerance | Staged via temporary file and committed via atomic filesystem rename; prevents partial reads or torn snapshots. |
| `INV-ACC-07` | Idempotent CAMT Ingestion | Data Integrity | Balances matched strictly by normalized IBAN; returns deterministic German status feedback (`aktualisiert`, `unverändert`). |
| `INV-ACC-08` | Deterministic Fail-Closed Error | Predictable Failure Modes | Typed standard library exceptions (`FileNotFoundError`, `ValueError`); never falls through or fails silently. |
| `INV-ACC-09` | RunAsInvoker Non-Elevation | Execution Privilege | Operates strictly in unprivileged user space; zero administrative or elevated privileges required on Windows, Linux, or macOS. |
| `INV-ACC-10` | 48h SLA & Security Policy | Vulnerability Management | Formal 48h response and 5-day triage commitment documented in `SECURITY.md` and verified by automated contract tests. |

---

## RunAsInvoker & Privilege Certification

`accounts-core` is certified to operate under the `RunAsInvoker` execution model:
- **Zero Elevation Required:** Runs completely within standard user privileges on Windows (`UAC: asInvoker`), Linux (unprivileged UID), and macOS.
- **Zero Daemon Overhead:** Does not spawn background daemons, listen on local network ports, or require root/administrator access.
- **Copyleft Isolation:** 100% MIT licensed code executing on Python Software Foundation (PSF-2.0) runtime. Zero GPL, AGPL, or viral copyleft contamination.

---

## Development & Test Dependencies

The following tools and libraries are utilized exclusively during development, code style verification, packaging, and automated contract testing:

| Package / Tool | Version Spec | License | Scope | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| [pytest](https://pytest.org/) | `>=8.0` | MIT | `[dev]` | Automated unit, contract, regression, and metadata test execution |
| [ruff](https://github.com/astral-sh/ruff) | `>=0.5` | MIT OR Apache-2.0 | `[dev]` | High-performance Python linter, style enforcer, and AST validation |
| [setuptools](https://github.com/pypa/setuptools) | `>=68.0` | MIT | `[build-system]` | Standard PEP 517/PEP 621 build backend and packaging |

---

## External Tools & Binaries (System Level)

| Binary / Tool | Recommended Version | License | Scope | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| [Python](https://www.python.org/) | `>=3.10` | PSF License | System Runtime | Multi-OS execution environment (`Windows`, `Linux`, `macOS`) |
| [Git](https://git-scm.com/) | `>=2.40` | GPL-2.0 | Version Control | Plan-D source-of-truth management and release tagging |

---

## License Texts & Attribution

### MIT License (`accounts-core`, `pytest`, `setuptools`, `ruff`)

```text
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Python Software Foundation License (PSF) (`Python Standard Library`)

```text
PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
--------------------------------------------

1. This LICENSE AGREEMENT is between the Python Software Foundation ("PSF"), and
the Individual or Organization ("Licensee") accessing and otherwise using this
software ("Python") in source or binary form and its associated documentation.

2. Subject to the terms and conditions of this License Agreement, PSF hereby
grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce,
analyze, test, perform and/or display publicly, prepare derivative works,
distribute, and otherwise use Python alone or in any derivative version,
provided, however, that PSF's License Agreement and PSF's notice of copyright,
i.e., "Copyright (c) 2001-2026 Python Software Foundation; All Rights Reserved"
are retained in Python alone or in any derivative version prepared by Licensee.

3. In the event Licensee prepares a derivative work that is based on or
incorporates Python or any part thereof, and wants to make the derivative work
available to others as provided herein, then Licensee hereby agrees to include in
any such work a brief summary of the changes made to Python.

4. PSF is making Python available to Licensee on an "AS IS" basis. PSF MAKES NO
REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED. BY WAY OF EXAMPLE, BUT NOT
LIMITATION, PSF MAKES NO AND DISCLAIMS ANY REPRESENTATION OR WARRANTY OF
MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF
PYTHON WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.

5. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON FOR ANY
INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS A RESULT OF MODIFYING,
DISTRIBUTING, OR OTHERWISE USING PYTHON, OR ANY DERIVATIVE THEREOF, EVEN IF
ADVISED OF THE POSSIBILITY THEREOF.
```
