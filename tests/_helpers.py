from pathlib import Path


TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent


def fixture_path(*parts: str) -> Path:
    """Build an absolute path to a test fixture under tests/golden/fixtures."""
    return TESTS_DIR / "golden" / "fixtures" / Path(*parts)


def golden_path(*parts: str) -> Path:
    """Build an absolute path to a test golden file under tests/golden."""
    return TESTS_DIR / "golden" / Path(*parts)
