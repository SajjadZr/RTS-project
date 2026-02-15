"""Pytest fixtures."""

from pathlib import Path

import pytest

from rts_sim.config import Config, load_config


@pytest.fixture
def config() -> Config:
    """Default config (no file)."""
    return load_config(None)


@pytest.fixture
def config_with_file(tmp_path: Path) -> Config:
    """Config loaded from a temp YAML file."""
    cfg = tmp_path / "config.yaml"
    cfg.write_text("gen:\n  n_tasks: 5\nseed: 42\n")
    return load_config(cfg)
