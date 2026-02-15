"""Config loading tests."""

from pathlib import Path

import pytest

from rts_sim.config import Config, load_config, resolve_config_path


def test_load_config_defaults() -> None:
    """Load with no file returns PDF defaults."""
    cfg = load_config(None)
    assert cfg.gen.n_tasks >= 1
    assert cfg.gen.erdos_renyi_p == 0.1
    assert cfg.system.m_min == 2
    assert cfg.system.m_max == 64
    assert cfg.resources.total_access_options == [10, 30, 50, 80, 150]


def test_load_config_from_file(config_with_file: Config) -> None:
    """Load from YAML overrides defaults."""
    cfg = config_with_file
    assert cfg.gen.n_tasks == 5
    assert cfg.seed == 42


def test_resolve_config_path_none() -> None:
    """resolve_config_path(None) looks for config.yaml/config.json."""
    # May or may not find file depending on cwd
    p = resolve_config_path(None)
    assert p is None or p.exists()


def test_resolve_config_path_explicit(tmp_path: Path) -> None:
    """Explicit path is returned if exists."""
    f = tmp_path / "custom.yaml"
    f.write_text("seed: 1")
    got = resolve_config_path(str(f))
    assert got is not None and got.exists() and got.samefile(f)
