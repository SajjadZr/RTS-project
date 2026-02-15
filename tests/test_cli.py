"""CLI smoke tests."""

import subprocess
import sys
from pathlib import Path


def test_help() -> None:
    """python -m rts_sim --help runs and lists commands."""
    r = subprocess.run(
        [sys.executable, "-m", "rts_sim", "--help"],
        cwd=Path(__file__).resolve().parent.parent,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0
    assert "generate" in r.stdout
    assert "run" in r.stdout
    assert "plot" in r.stdout
    assert "all" in r.stdout


def test_all_dry_run() -> None:
    """python -m rts_sim all --dry-run validates config and creates dirs."""
    root = Path(__file__).resolve().parent.parent
    r = subprocess.run(
        [sys.executable, "-m", "rts_sim", "all", "--dry-run"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0
    assert "Dry run" in r.stdout or "dry" in r.stdout.lower()
