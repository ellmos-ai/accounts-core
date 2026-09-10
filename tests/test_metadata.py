"""Automated metadata, security policy, CI integrity, and documentation parity contract tests."""

from pathlib import Path

try:
    import tomllib
except ImportError:  # pragma: no cover - Python 3.10 compatibility
    import tomli as tomllib

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_pyproject_structure_and_pep621_urls():
    """Verify pyproject.toml contains required PEP 621 metadata, version 0.1.1,
    and ecosystem URLs."""
    pyproject_path = REPO_ROOT / "pyproject.toml"
    assert pyproject_path.is_file(), "pyproject.toml must exist"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))

    project = data.get("project", {})
    assert project.get("name") == "accounts-core"
    assert project.get("version") == "0.1.1"
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
    assert urls.get("Parent Organization") == "https://github.com/ellmos-ai"
    assert urls.get("Umbrella Ecosystem") == "https://github.com/open-bricks"


def test_pytest_ini_options_configured():
    """Verify pytest configuration includes pythonpath and verbose reporting options."""
    pyproject_path = REPO_ROOT / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))

    ini_opts = data.get("tool", {}).get("pytest", {}).get("ini_options", {})
    assert ini_opts.get("testpaths") == ["tests"]
    assert "." in ini_opts.get("pythonpath", []) or "src" in ini_opts.get("pythonpath", [])
    assert "-ra -v" in ini_opts.get("addopts", "")


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
        "badge/version-0.1.1-blue.svg",
        "actions/workflows/ci.yml/badge.svg",
        "tests-26%20passed%20%7C%20100%25%20green-brightgreen.svg",
        "python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg",
        "platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg",
        "privacy-100%25%20Local--First%20%7C%20Zero--Egress-brightgreen.svg",
        "security%20SLA-48h%20response%20%7C%205d%20triage-blue.svg",
        "code%20style-ruff-000000.svg",
        "ecosystem-ellmos--ai-informational.svg",
        "umbrella-open--bricks-informational.svg",
        "LLM-llms.txt-blueviolet.svg",
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

    assert "## Last-checked: 2026-09-09" in content
    assert "0.1.1" in content
    assert "26" in content
    assert "SECURITY.md" in content
    assert "pyproject.toml" in content
    assert "CHANGELOG.md" in content
    assert "ellmos-module.v2.json" in content


def test_changelog_release_entry():
    """Verify CHANGELOG.md contains the 0.1.1 release entry."""
    changelog_path = REPO_ROOT / "CHANGELOG.md"
    assert changelog_path.is_file(), "CHANGELOG.md must exist"
    content = changelog_path.read_text(encoding="utf-8")

    assert "## [0.1.1] - 2026-09-09" in content


def test_version_parity_across_artifacts():
    """Verify version 0.1.1 is consistent across pyproject.toml, ellmos-module,
    __init__.py, and llms.txt."""
    pyproject_path = REPO_ROOT / "pyproject.toml"
    pyproject_data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    assert pyproject_data["project"]["version"] == "0.1.1"

    import json
    module_path = REPO_ROOT / "ellmos-module.v2.json"
    module_data = json.loads(module_path.read_text(encoding="utf-8"))
    assert module_data["version"] == "0.1.1"

    init_path = REPO_ROOT / "src" / "accounts_core" / "__init__.py"
    init_content = init_path.read_text(encoding="utf-8")
    assert '__version__ = "0.1.1"' in init_content

    llms_path = REPO_ROOT / "llms.txt"
    llms_content = llms_path.read_text(encoding="utf-8")
    assert "- Version: 0.1.1" in llms_content
