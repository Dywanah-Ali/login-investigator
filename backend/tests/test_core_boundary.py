"""The core stays plain Python: the screens, the API and the agent's tools call it, and it never
imports a shell. v1 forbade Streamlit; v2 also forbids FastAPI and Starlette, which FastAPI is
built on."""

import ast
from pathlib import Path

import pytest

CORE = Path(__file__).resolve().parent.parent / "login_investigator"

SHELLS = ["streamlit", "fastapi", "starlette"]


def imported_modules(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            yield from (alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            yield node.module


def core_files():
    """Every Python file in the core, including any subpackage added later."""
    return sorted(CORE.rglob("*.py"))


# v1's test, kept unchanged so the copied suite stays v1's. The parametrised test below covers it too.
def test_no_core_module_imports_streamlit():
    files = sorted(CORE.glob("*.py"))
    assert files
    offenders = [
        f.name for f in files if any(m.split(".")[0] == "streamlit" for m in imported_modules(f))
    ]
    assert offenders == []


@pytest.mark.parametrize("shell", SHELLS)
def test_no_core_module_imports_a_shell(shell):
    files = core_files()
    assert files
    offenders = [
        str(f.relative_to(CORE))
        for f in files
        if any(m.split(".")[0] == shell for m in imported_modules(f))
    ]
    assert offenders == [], f"core imports {shell}: {offenders}"
