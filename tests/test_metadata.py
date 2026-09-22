"""Automated metadata, security policy, CI integrity, and documentation parity contract tests."""

from pathlib import Path

try:
    import tomllib
except ImportError:  # pragma: no cover - Python 3.10 compatibility
    import tomli as tomllib

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_pyproject_structure_and_pep621_urls():
    """Verify pyproject.toml contains required PEP 621 metadata, version 0.1.4,
    and ecosystem URLs."""
    pyproject_path = REPO_ROOT / "pyproject.toml"
    assert pyproject_path.is_file(), "pyproject.toml must exist"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))

    project = data.get("project", {})
    assert project.get("name") == "accounts-core"
    assert project.get("version") == "0.1.4"
    assert project.get("requires-python") == ">=3.10"
    assert project.get("license") == "MIT"

    classifiers = project.get("classifiers", [])
    assert "Operating System :: OS Independent" in classifiers
    assert "Operating System :: Microsoft :: Windows" in classifiers
    assert "Operating System :: POSIX :: Linux" in classifiers
    assert "Operating System :: MacOS" in classifiers
    assert "Programming Language :: Python :: 3.10" in classifiers
    assert "Programming Language :: Python :: 3.13" in classifiers

    urls = project.get("urls", {})
    assert urls.get("Homepage") == "https://github.com/ellmos-ai/accounts-core"
    assert urls.get("Repository") == "https://github.com/ellmos-ai/accounts-core"
    assert urls.get("Documentation") == "https://github.com/ellmos-ai/accounts-core#readme"
    assert urls.get("Issues") == "https://github.com/ellmos-ai/accounts-core/issues"
    assert urls.get("Changelog") == "https://github.com/ellmos-ai/accounts-core/blob/main/CHANGELOG.md"
    assert urls.get("Security") == "https://github.com/ellmos-ai/accounts-core/blob/main/SECURITY.md"
    assert urls.get("Marketing Log") == "https://github.com/ellmos-ai/accounts-core/blob/main/MARKETING-LOG.txt"
    assert urls.get("Third-Party Licenses") == "https://github.com/ellmos-ai/accounts-core/blob/main/THIRD_PARTY_LICENSES.md"
    assert urls.get("Notice") == "https://github.com/ellmos-ai/accounts-core/blob/main/NOTICE"
    assert urls.get("LLM Ready") == "https://raw.githubusercontent.com/ellmos-ai/accounts-core/main/llms.txt"
    assert urls.get("Parent Organization") == "https://github.com/ellmos-ai"
    assert urls.get("Umbrella Ecosystem") == "https://github.com/open-bricks"


def test_pytest_ini_options_configured():
    """Verify pytest configuration includes pythonpath, norecursedirs, and verbose reporting options."""
    pyproject_path = REPO_ROOT / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))

    ini_opts = data.get("tool", {}).get("pytest", {}).get("ini_options", {})
    assert ini_opts.get("testpaths") == ["tests"]
    assert "." in ini_opts.get("pythonpath", []) or "src" in ini_opts.get("pythonpath", [])
    assert "-ra -v" in ini_opts.get("addopts", "")
    assert ini_opts.get("norecursedirs") == [".git", ".pytest_cache", "__pycache__", "build", "dist", ".venv", "venv"]


def test_gitignore_hygiene_patterns():
    """Verify .gitignore includes multi-host conflicts, multi-agent locks, and caches."""
    gitignore_path = REPO_ROOT / ".gitignore"
    assert gitignore_path.is_file(), ".gitignore must exist"
    content = gitignore_path.read_text(encoding="utf-8")

    # Multi-Host-Synchronisationskonflikte
    assert "*-conflict-*" in content
    assert "*.sync-conflict-*" in content
    assert "*.conflict" in content
    assert "*-CONFLIT-*" in content
    assert "*.sync-temp-*" in content

    # Multi-Agent Locks
    assert "LOCK" in content
    assert "LOCK.*" in content
    assert "*.lock" in content
    assert "LOCK*.txt" in content
    assert "LOCK.permissions.json" in content

    # Test- and coverage caches
    assert ".coverage" in content
    assert "coverage/" in content
    assert "htmlcov/" in content
    assert "wheelhouse/" in content
    assert ".wheel-smoke/" in content

    # Temporary and editor backups
    assert "*.tmp" in content
    assert "*.bak" in content
    assert "*.swp" in content
    assert "*~" in content
    assert "*.log" in content


def test_ci_workflow_hardening():
    """Verify GitHub Actions CI workflow defines concurrency, bytecode gate, and test execution."""
    ci_path = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    assert ci_path.is_file(), ".github/workflows/ci.yml must exist"
    content = ci_path.read_text(encoding="utf-8")

    assert "concurrency:" in content
    assert "cancel-in-progress: true" in content
    assert "python -m compileall -q src tests" in content
    assert "python -m ruff check src tests" in content
    assert "python -m pytest -ra -v" in content
    assert "macos-latest" in content
    assert "ubuntu-latest" in content
    assert "windows-latest" in content
    assert "3.10" in content
    assert "3.13" in content


def test_security_policy_slas_and_contacts():
    """Verify SECURITY.md defines supported versions, 48h response SLA, 5-day triage,
    and contacts."""
    sec_path = REPO_ROOT / "SECURITY.md"
    assert sec_path.is_file(), "SECURITY.md must exist"
    content = sec_path.read_text(encoding="utf-8")

    # Supported versions
    assert "Supported Versions" in content
    assert "0.1.x" in content

    # SLAs
    assert "48 hours" in content
    assert "48 Stunden" in content
    assert "5 business days" in content
    assert "5 Werktagen" in content

    # Contacts
    assert "security@open-bricks.org" in content
    assert "security@ellmos.ai" in content
    assert "support@lukasgeiger.com" in content
    assert "lukas@open-bricks.org" in content

    # Advisory URL & Architecture
    assert "https://github.com/ellmos-ai/accounts-core/security/advisories/new" in content
    assert "Local-First & Zero-Egress" in content
    assert "User-Mode Non-Elevation" in content


def test_readme_badges_parity():
    """Verify README.md and README_de.md include synchronized status badges."""
    readme_en = REPO_ROOT / "README.md"
    readme_de = REPO_ROOT / "README_de.md"
    assert readme_en.is_file(), "README.md must exist"
    assert readme_de.is_file(), "README_de.md must exist"

    en_text = readme_en.read_text(encoding="utf-8")
    de_text = readme_de.read_text(encoding="utf-8")

    expected_badges = [
        "badge/version-0.1.4-blue.svg",
        "actions/workflows/ci.yml/badge.svg",
        "tests-58%20passed%20%7C%20100%25%20green-brightgreen.svg",
        "python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg",
        "platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg",
        "privacy-100%25%20Local--First%20%7C%20Zero--Egress-brightgreen.svg",
        "security%20SLA-48h%20response%20%7C%205d%20triage-blue.svg",
        "code%20style-ruff-000000.svg",
        "ecosystem-ellmos--ai-informational.svg",
        "umbrella-open--bricks-informational.svg",
        "marketing%20log-blueprints-informational.svg",
        "LLM-llms.txt-blueviolet.svg",
        "attribution-NOTICE-blue.svg",
        "license-MIT-green.svg",
    ]

    for badge in expected_badges:
        assert badge in en_text, f"Missing badge '{badge}' in README.md"
        assert badge in de_text, f"Missing badge '{badge}' in README_de.md"


def test_llms_txt_current_timestamp_and_links():
    """Verify llms.txt contains the current check timestamp, version, and canonical references."""
    llms_path = REPO_ROOT / "llms.txt"
    assert llms_path.is_file(), "llms.txt must exist"
    content = llms_path.read_text(encoding="utf-8")

    assert "## Last-checked: 2026-09-22" in content
    assert "0.1.4" in content
    assert "NOTICE" in content
    assert "SECURITY.md" in content
    assert "pyproject.toml" in content
    assert "CHANGELOG.md" in content
    assert "ellmos-module.v2.json" in content
    assert "MARKETING-LOG.txt" in content
    assert "THIRD_PARTY_LICENSES.md" in content
    assert "TODO.md" in content
    assert "INV-ACC-01" in content
    assert "INV-ACC-10" in content


def test_changelog_release_entry():
    """Verify CHANGELOG.md contains Unreleased and past release entries."""
    changelog_path = REPO_ROOT / "CHANGELOG.md"
    assert changelog_path.is_file(), "CHANGELOG.md must exist"
    content = changelog_path.read_text(encoding="utf-8")

    assert "## [Unreleased]" in content
    assert "## [0.1.4] - 2026-09-20" in content
    assert "## [0.1.3] - 2026-09-12" in content
    assert "## [0.1.2] - 2026-09-11" in content
    assert "## [0.1.1] - 2026-09-09" in content


def test_version_parity_across_artifacts():
    """Verify version 0.1.4 is consistent across pyproject.toml, ellmos-module,
    __init__.py, and llms.txt."""
    pyproject_path = REPO_ROOT / "pyproject.toml"
    pyproject_data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    assert pyproject_data["project"]["version"] == "0.1.4"

    import json
    module_path = REPO_ROOT / "ellmos-module.v2.json"
    module_data = json.loads(module_path.read_text(encoding="utf-8"))
    assert module_data["version"] == "0.1.4"

    init_path = REPO_ROOT / "src" / "accounts_core" / "__init__.py"
    init_content = init_path.read_text(encoding="utf-8")
    assert '__version__ = "0.1.4"' in init_content

    llms_path = REPO_ROOT / "llms.txt"
    llms_content = llms_path.read_text(encoding="utf-8")
    assert "- Version: 0.1.4" in llms_content


def test_marketing_log_structure_and_blueprints():
    """Verify MARKETING-LOG.txt exists, contains target personas, keywords,
    directory recommendations, and 3 integration blueprints."""
    mkt_path = REPO_ROOT / "MARKETING-LOG.txt"
    assert mkt_path.is_file(), "MARKETING-LOG.txt must exist"
    content = mkt_path.read_text(encoding="utf-8")

    assert "## 1. Target Personas & Audiences" in content
    assert "FinTech & Local Accounting Engineers" in content
    assert "Privacy-by-Design & Local-First Architects" in content
    assert "Multi-Source Banking Data Integrators" in content
    assert "Autonomous AI Agent Framework Builders" in content

    assert "## 2. Discoverability & SEO Keywords" in content
    assert "bank-accounts" in content
    assert "iban-validation" in content
    assert "camt-parser" in content

    assert "## 3. Directory & Ecosystem Recommendations" in content
    assert "Awesome Python" in content
    assert "Awesome Privacy" in content

    assert "## 4. Integration Blueprints" in content
    assert "### Blueprint 1: Standard Account Lifecycle & Persistence" in content
    assert "### Blueprint 2: Idempotent CAMT Balance Ingestion" in content
    assert "### Blueprint 3: Privacy-Preserving Transit Projection for Agents / UI" in content


def test_readme_flowchart_mermaid_syntax():
    """Verify both READMEs include flowchart TD with valid quoting per HOOK-BANNER-ASSET-01."""
    import re
    edge_re = re.compile(r"((?:--+>|<-+>|-\.-+>|==+>)\|)([^|\r\n]+)(\|)")

    for fname in ("README.md", "README_de.md"):
        path = REPO_ROOT / fname
        assert path.is_file(), f"{fname} must exist"
        text = path.read_text(encoding="utf-8")
        assert "```mermaid\nflowchart TD" in text, f"{fname} must contain flowchart TD"

        # Check all edge labels with parentheses or special chars are double-quoted
        for match in edge_re.finditer(text):
            label = match.group(2).strip()
            if any(c in label for c in "()[]{}"):
                assert label.startswith('"') and label.endswith('"'), (
                    f"Edge label in {fname} has unquoted special chars: {label}"
                )


def test_readme_sequencediagram_mermaid_syntax():
    """Verify both READMEs include sequenceDiagram with autonumber and valid syntax."""
    for fname in ("README.md", "README_de.md"):
        path = REPO_ROOT / fname
        assert path.is_file(), f"{fname} must exist"
        text = path.read_text(encoding="utf-8")
        assert "```mermaid\nsequenceDiagram" in text, f"{fname} must contain sequenceDiagram"
        assert "autonumber" in text, f"{fname} sequenceDiagram must contain autonumber"
        assert "publish_transit_projection" in text, f"{fname} sequenceDiagram must detail transit projection"


def test_governance_invariants_documented():
    """Verify all 10 governance invariants (INV-ACC-01 to INV-ACC-10) are documented in both READMEs."""
    expected_invariants = [
        "INV-ACC-01",
        "INV-ACC-02",
        "INV-ACC-03",
        "INV-ACC-04",
        "INV-ACC-05",
        "INV-ACC-06",
        "INV-ACC-07",
        "INV-ACC-08",
        "INV-ACC-09",
        "INV-ACC-10",
    ]

    for fname in ("README.md", "README_de.md"):
        path = REPO_ROOT / fname
        content = path.read_text(encoding="utf-8")
        for inv in expected_invariants:
            assert inv in content, f"Missing invariant {inv} in {fname}"


def test_ecosystem_sister_repositories_table():
    """Verify both READMEs include the ecosystem cross-linking table."""
    expected_repos = [
        "bach",
        "sqlite-transit-sync",
        "assistant-core",
        "open-ocean",
        "report-forge",
        "open-bricks",
    ]

    for fname in ("README.md", "README_de.md"):
        path = REPO_ROOT / fname
        content = path.read_text(encoding="utf-8")
        for repo in expected_repos:
            assert repo in content, f"Missing ecosystem repo {repo} in {fname}"


def test_readme_bilingual_section_parity():
    """Verify 1:1 section header parity between README.md and README_de.md."""
    en_path = REPO_ROOT / "README.md"
    de_path = REPO_ROOT / "README_de.md"

    en_h2 = [line.strip() for line in en_path.read_text(encoding="utf-8").splitlines() if line.startswith("## ")]
    de_h2 = [line.strip() for line in de_path.read_text(encoding="utf-8").splitlines() if line.startswith("## ")]

    assert len(en_h2) == len(de_h2), (
        f"H2 header count mismatch between README.md ({len(en_h2)}) and README_de.md ({len(de_h2)})"
    )
    assert len(en_h2) == 19, f"Expected exactly 19 H2 sections (1 Table of Contents + 18 content sections), found {len(en_h2)}"


def test_third_party_licenses_inventory_and_zero_dependencies():
    """Verify THIRD_PARTY_LICENSES.md exists and runtime dependencies invariant is enforced."""
    lic_path = REPO_ROOT / "THIRD_PARTY_LICENSES.md"
    assert lic_path.is_file(), "THIRD_PARTY_LICENSES.md must exist"
    content = lic_path.read_text(encoding="utf-8")
    assert "Zero-Runtime-Dependency" in content or "Zero External Runtime Dependencies" in content
    assert "MIT License" in content

    pyproject_path = REPO_ROOT / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    assert data.get("project", {}).get("dependencies") == []


def test_pep639_license_files_metadata():
    """Verify PEP 639 license-files declaration in pyproject.toml."""
    pyproject_path = REPO_ROOT / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    license_files = data.get("project", {}).get("license-files", [])
    assert "LICENSE" in license_files
    assert "NOTICE" in license_files
    assert "THIRD_PARTY_LICENSES.md" in license_files


def test_todo_status_table_and_gate_readiness():
    """Verify TODO.md contains a structured STATUS table and formalized tasks."""
    todo_path = REPO_ROOT / "TODO.md"
    assert todo_path.is_file(), "TODO.md must exist"
    content = todo_path.read_text(encoding="utf-8")
    assert "## STATUS" in content
    assert "| Category" in content or "|Category" in content
    assert "0.1.4" in content


def test_gitignore_complete_gate_entries():
    """Verify .gitignore contains all mandatory Gate 1 entries."""
    gitignore_path = REPO_ROOT / ".gitignore"
    content = gitignore_path.read_text(encoding="utf-8")
    for req in ["__pycache__", "*.pyc", ".env", "*.db", ".venv/", ".idea/", ".vscode/", "data/"]:
        req_clean = req.rstrip("/")
        assert req in content or req_clean in content, f"Missing required gitignore entry: {req}"


def test_final_gate_check_compliance():
    """Verify Gates 1-10 release readiness rules in a path-neutral manner."""
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    for req in ["__pycache__", "*.pyc", ".env", "*.db", ".venv/", ".idea/", ".vscode/", "data/"]:
        req_clean = req.rstrip("/")
        assert req in gitignore or req_clean in gitignore, f"Missing required .gitignore entry: {req}"

    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    first_50 = "\n".join(readme_en.splitlines()[:50])
    for indicator in ["Dokumentation", "Voraussetzungen", "Einleitung", "Beschreibung"]:
        assert indicator not in first_50, f"German indicator {indicator} in first 50 lines of README.md"

    assert (REPO_ROOT / "LICENSE").is_file(), "LICENSE must exist"
    assert (REPO_ROOT / "TODO.md").is_file(), "TODO.md must exist"
    todo_text = (REPO_ROOT / "TODO.md").read_text(encoding="utf-8")
    assert "## STATUS" in todo_text
    assert "| Category" in todo_text or "|Category" in todo_text


def test_ci_timeout_minutes_configured():
    """Verify .github/workflows/ci.yml configures timeout-minutes: 15 on the test matrix."""
    ci_path = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    assert ci_path.is_file(), "ci.yml must exist"
    content = ci_path.read_text(encoding="utf-8")
    assert "timeout-minutes: 15" in content


def test_ci_stale_workflow_present():
    """Verify .github/workflows/stale.yml exists and configures automated lifecycle."""
    stale_path = REPO_ROOT / ".github" / "workflows" / "stale.yml"
    assert stale_path.is_file(), "stale.yml must exist"
    content = stale_path.read_text(encoding="utf-8")
    assert "actions/stale@v9" in content or "actions/stale" in content
    assert "schedule:" in content
    assert "issues: write" in content
    assert "pull-requests: write" in content


def test_pep621_llm_ready_url_and_ruff_lint():
    """Verify pyproject.toml defines LLM Ready URL and tool.ruff.lint rules."""
    pyproject_path = REPO_ROOT / "pyproject.toml"
    assert pyproject_path.is_file(), "pyproject.toml must exist"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))

    urls = data.get("project", {}).get("urls", {})
    assert "LLM Ready" in urls
    assert urls["LLM Ready"] == "https://raw.githubusercontent.com/ellmos-ai/accounts-core/main/llms.txt"

    lint = data.get("tool", {}).get("ruff", {}).get("lint", {})
    assert "select" in lint
    select_rules = lint.get("select", [])
    for rule in ["E4", "E7", "E9", "F", "W", "B", "SIM", "C4", "RUF"]:
        assert rule in select_rules, f"Rule {rule} missing from tool.ruff.lint.select"


def test_gitignore_multihost_conflict_patterns():
    """Verify .gitignore contains multi-host synchronization and lock patterns."""
    gitignore_path = REPO_ROOT / ".gitignore"
    content = gitignore_path.read_text(encoding="utf-8")
    for pattern in ["* (kopie)*", "* (copy)*", "*-WORKSTATION*", "uv.lock", "!package-lock.json"]:
        assert pattern in content, f"Missing pattern {pattern} in .gitignore"


def test_readme_quick_navigation_anchors_parity():
    """Verify 18-point quick navigation anchors parity across README.md and README_de.md."""
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    en_anchors = [
        "key-features",
        "visual-architecture",
        "sequence-lifecycle",
        "target-personas--discoverability",
        "comparative-matrix--alternatives",
        "contract--domain-boundaries",
        "privacy-allowlist-projection",
        "governance--runtime-invariants",
        "installation",
        "quickstart--usage-guide",
        "camt-balance-ingestion",
        "transit-publisher-specification",
        "sibling-tools--ecosystem",
        "third-party-licenses--transparency",
        "repository-structure",
        "development--test-matrix",
        "security-policy--contact",
        "statutory-notice--liability-limitation",
    ]

    de_anchors = [
        "hauptmerkmale",
        "visuelle-architektur",
        "sequenz-lebenszyklus",
        "zielgruppen--auffindbarkeit",
        "vergleichsmatrix--alternativen",
        "vertrag--domaenengrenzen",
        "datenschutz-allowlist-projektion",
        "governance--laufzeit-invarianten",
        "installation",
        "schnellstart--anwendungsbeispiele",
        "camt-salden-verarbeitung",
        "transit-publisher-spezifikation",
        "geschwisterwerkzeuge--oekosystem",
        "drittanbieter-lizenzen--transparenz",
        "repository-struktur",
        "entwicklung--testmatrix",
        "sicherheitsrichtlinie--kontakt",
        "gesetzlicher-hinweis--haftungsbeschraenkung",
    ]

    assert len(en_anchors) == 18
    assert len(de_anchors) == 18

    for anchor in en_anchors:
        assert f'<a id="{anchor}"></a>' in readme_en, f"Anchor '{anchor}' missing in README.md"
        assert f"(#{anchor})" in readme_en, f"TOC link '#{anchor}' missing in README.md"

    for anchor in de_anchors:
        assert f'<a id="{anchor}"></a>' in readme_de, f"Anchor '{anchor}' missing in README_de.md"
        assert f"(#{anchor})" in readme_de, f"TOC link '#{anchor}' missing in README_de.md"


def test_target_personas_and_high_intent_keywords():
    """Verify target personas [PERSONA-01] to [PERSONA-04] and high-intent SEO queries."""
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")
    mkt = (REPO_ROOT / "MARKETING-LOG.txt").read_text(encoding="utf-8")

    for persona in ["[PERSONA-01]", "[PERSONA-02]", "[PERSONA-03]", "[PERSONA-04]"]:
        assert persona in readme_en, f"{persona} missing in README.md"
        assert persona in readme_de, f"{persona} missing in README_de.md"

    for query in ["camt balance import", "privacy-safe bank balance projection"]:
        assert query in readme_en, f"Query '{query}' missing in README.md"
        assert query in readme_de, f"Query '{query}' missing in README_de.md"
        assert query in mkt, f"Query '{query}' missing in MARKETING-LOG.txt"


def test_comparative_matrix_alternatives():
    """Verify 10-dimension comparative matrix vs. 4 alternatives in both READMEs."""
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    alternatives = [
        "accounts-core",
        "Ad-Hoc",
        "Odoo",
        "Tryton",
        "Plaid",
        "Tink",
    ]

    for alt in alternatives:
        assert alt in readme_en, f"Alternative '{alt}' missing in README.md"
        assert alt in readme_de, f"Alternative '{alt}' missing in README_de.md"


def test_statutory_notice_bgb_521():
    """Verify statutory notice (§ 521 BGB Gefälligkeitsrecht) in documentation and llms.txt."""
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")
    llms = (REPO_ROOT / "llms.txt").read_text(encoding="utf-8")

    assert "521 BGB" in readme_en, "§ 521 BGB missing in README.md"
    assert "521 BGB" in readme_de, "§ 521 BGB missing in README_de.md"
    assert "521 BGB" in llms, "§ 521 BGB missing in llms.txt"


def test_third_party_licenses_audit_recency():
    """Verify THIRD_PARTY_LICENSES.md audit date, Level 1 SBOM, and Invariant Matrix."""
    lic_path = REPO_ROOT / "THIRD_PARTY_LICENSES.md"
    assert lic_path.is_file(), "THIRD_PARTY_LICENSES.md must exist"
    content = lic_path.read_text(encoding="utf-8")

    assert "2026-09-22" in content or "2026-09-20" in content, "Audit date missing in THIRD_PARTY_LICENSES.md"
    assert "[NOTICE](NOTICE)" in content
    assert "Level 1 SBOM" in content or "Level 1 Software Bill of Materials" in content
    assert "RunAsInvoker" in content
    for inv in [f"INV-ACC-{i:02d}" for i in range(1, 11)]:
        assert inv in content, f"Invariant {inv} missing in THIRD_PARTY_LICENSES.md"


def test_run_as_invoker_user_mode_invariant():
    """Verify INV-ACC-09 (RunAsInvoker user-mode non-elevation) across all documentation."""
    for fname in ["README.md", "README_de.md", "THIRD_PARTY_LICENSES.md", "llms.txt"]:
        content = (REPO_ROOT / fname).read_text(encoding="utf-8")
        assert "INV-ACC-09" in content, f"INV-ACC-09 missing in {fname}"
        assert "RunAsInvoker" in content, f"RunAsInvoker missing in {fname}"


def test_sla_commitments_security_policy_invariant():
    """Verify INV-ACC-10 (48h response & 5-day triage SLA) across all documentation."""
    for fname in ["SECURITY.md", "README.md", "README_de.md", "llms.txt"]:
        content = (REPO_ROOT / fname).read_text(encoding="utf-8")
        assert "48" in content, f"48h response missing in {fname}"
        assert "5" in content, f"5-day triage missing in {fname}"
    assert "INV-ACC-10" in (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "INV-ACC-10" in (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")
    assert "INV-ACC-10" in (REPO_ROOT / "llms.txt").read_text(encoding="utf-8")


def test_license_and_bom_level_certification():
    """Verify Level 1 SBOM certification, zero dependencies, and MIT license consistency."""
    lic_content = (REPO_ROOT / "THIRD_PARTY_LICENSES.md").read_text(encoding="utf-8")
    assert "Level 1 SBOM" in lic_content
    assert "Zero External Runtime Dependencies" in lic_content
    assert "PSF" in lic_content
    assert "MIT" in lic_content

    pyproject_data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject_data["project"]["dependencies"] == []
    assert pyproject_data["project"]["license"] == "MIT"


def test_notice_file_canonical_attribution():
    """Verify NOTICE file exists and declares canonical attribution and umbrella links."""
    notice_path = REPO_ROOT / "NOTICE"
    assert notice_path.is_file(), "NOTICE must exist"
    content = notice_path.read_text(encoding="utf-8")
    assert "accounts-core" in content
    assert "Lukas Geiger" in content
    assert "ellmos-ai" in content
    assert "open-bricks" in content
    assert "MIT License" in content
    assert "THIRD_PARTY_LICENSES.md" in content


def test_welcome_workflow_lifecycle_hardening():
    """Verify .github/workflows/welcome.yml enforces first-interaction@v3, timeout, and concurrency."""
    welcome_path = REPO_ROOT / ".github" / "workflows" / "welcome.yml"
    assert welcome_path.is_file(), "welcome.yml must exist"
    content = welcome_path.read_text(encoding="utf-8")
    assert "actions/first-interaction@v3" in content
    assert "timeout-minutes: 5" in content
    assert "concurrency:" in content
    assert "cancel-in-progress: true" in content
    assert "issues: write" in content
    assert "pull-requests: write" in content


def test_stale_workflow_lifecycle_hardening():
    """Verify .github/workflows/stale.yml enforces timeout-minutes: 10 and concurrency cancel-in-progress."""
    stale_path = REPO_ROOT / ".github" / "workflows" / "stale.yml"
    assert stale_path.is_file(), "stale.yml must exist"
    content = stale_path.read_text(encoding="utf-8")
    assert "timeout-minutes: 10" in content
    assert "concurrency:" in content
    assert "cancel-in-progress: true" in content


def test_gitignore_extended_lock_and_conflict_tokens():
    """Verify .gitignore includes multi-host, lock, and test cache patterns."""
    gitignore_path = REPO_ROOT / ".gitignore"
    content = gitignore_path.read_text(encoding="utf-8")
    for token in [
        "*-ASUS*",
        "*-Mac Studio*",
        "*-MacBook*",
        "LOCK.user.*",
        "LOCK.until.*",
        "LOCK.condition.*",
        ".automation-lock",
        ".hypothesis/",
        ".turbo/",
        ".nyc_output/",
    ]:
        assert token in content, f"Missing token '{token}' in .gitignore"


def test_marketing_log_audit_recency_and_sections():
    """Verify MARKETING-LOG.txt includes Section 7 and 2026-09-22 Pfad A audit."""
    mkt_path = REPO_ROOT / "MARKETING-LOG.txt"
    assert mkt_path.is_file(), "MARKETING-LOG.txt must exist"
    content = mkt_path.read_text(encoding="utf-8")
    assert "## 7. Technical Hygiene, CI Lifecycle Hardening & Lock Defense Audit (2026-09-22)" in content
    assert "NOTICE" in content
    assert "RunAsInvoker" in content


def test_unreleased_changelog_section():
    """Verify CHANGELOG.md contains ## [Unreleased] for Pfad A changes."""
    changelog_path = REPO_ROOT / "CHANGELOG.md"
    content = changelog_path.read_text(encoding="utf-8")
    assert "## [Unreleased]" in content
    assert "Repository Hygiene" in content
    assert "Level 1 SBOM" in content
