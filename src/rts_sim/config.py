"""Config system (YAML/JSON) with defaults matching the PDF.

PDF reference: Sections 1–6 (docs/project_info_1404_PQ_3.pdf).
Inputs: config file path(s), overrides.
Outputs: validated config dict or Pydantic model.
Invariants: defaults match PDF (m in [2,64], U_norm in [0.1,1], etc.).
"""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, field_validator


class GenConfig(BaseModel):
    """Task-set and DAG generation. PDF §2."""

    n_tasks: int = Field(ge=1, description="Number of tasks")
    nodes_per_task_min: int = Field(20, ge=1)
    nodes_per_task_max: int = Field(50, ge=1)
    erdos_renyi_p: float = Field(0.1, ge=0, le=1, description="Erdős–Rényi edge probability")
    period_values: list[float] = Field(default_factory=lambda: [2000.0, 4000.0, 6000.0])
    hi_fraction: float = Field(0.5, ge=0, le=1, description="Fraction of HI-criticality nodes")


class ResourcesConfig(BaseModel):
    """Resource request generation and segments. PDF §3–4."""

    n_resources_min: int = Field(2, ge=1)
    n_resources_max: int = Field(8, ge=1)
    total_access_options: list[int] = Field(
        default_factory=lambda: [10, 30, 50, 80, 150]
    )
    csp_min: float = Field(0.1, ge=0, le=1)
    csp_max: float = Field(1.0, ge=0, le=1)


class SystemConfig(BaseModel):
    """Initial system setup. PDF §1."""

    m_min: int = Field(2, ge=1)
    m_max: int = Field(64, ge=1)
    U_norm_min: float = Field(0.1, ge=0, le=1)
    U_norm_max: float = Field(1.0, ge=0, le=1)


class PartitionConfig(BaseModel):
    """Federated and grouping-by-resource partitioning. PDF §5–6."""

    use_federated: bool = True
    use_grouping_by_resource: bool = True


class SchedConfig(BaseModel):
    """Baseline EDF/CA-EDF and lock protocol. PDF §5–6."""

    use_ca_edf: bool = True
    fifo_lock_hi_lo: bool = True
    deadlock_drop_low: bool = True


class Config(BaseModel):
    """Root config matching PDF defaults."""

    system: SystemConfig = Field(default_factory=SystemConfig)
    gen: GenConfig = Field(default_factory=GenConfig)
    resources: ResourcesConfig = Field(default_factory=ResourcesConfig)
    partition: PartitionConfig = Field(default_factory=PartitionConfig)
    sched: SchedConfig = Field(default_factory=SchedConfig)
    seed: int = 0
    output_dir: Path = Field(default=Path("output"))
    results_dir: Path = Field(default=Path("results"))
    plots_dir: Path = Field(default=Path("plots"))

    @field_validator("output_dir", "results_dir", "plots_dir", mode="before")
    @classmethod
    def coerce_path(cls, v: Any) -> Path:
        if isinstance(v, str):
            return Path(v)
        return v


def load_config(path: Path | None = None) -> Config:
    """Load config from YAML/JSON file; merge with defaults. PDF §1.

    Inputs: optional config file path.
    Outputs: Config instance.
    """
    defaults = Config()
    if path is None:
        return defaults
    path = Path(path)
    if not path.exists():
        return defaults
    raw: dict[str, Any] = {}
    with open(path, encoding="utf-8") as f:
        if path.suffix in (".yaml", ".yml"):
            raw = yaml.safe_load(f) or {}
        elif path.suffix == ".json":
            import json

            raw = json.load(f)
        else:
            return defaults
    merged = _deep_merge(defaults.model_dump(), raw)
    return Config.model_validate(merged)


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge override into base."""
    out = dict(base)
    for k, v in override.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def resolve_config_path(cli_path: str | None) -> Path | None:
    """Resolve config path from CLI. Prefer config.yaml then config.json."""
    if cli_path:
        p = Path(cli_path)
        return p if p.exists() else None
    for name in ("config.yaml", "config.yml", "config.json"):
        p = Path(name)
        if p.exists():
            return p
    return None
