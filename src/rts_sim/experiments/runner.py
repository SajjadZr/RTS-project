"""Experiment runner: single point and full sweep. PDF §1–6."""

from __future__ import annotations

from pathlib import Path

from rts_sim.config import Config
from rts_sim.models import ExperimentPoint, SimulationResult, TaskSet


def run_experiment(
    config: Config,
    point: ExperimentPoint,
    dry_run: bool = False,
) -> ExperimentPoint:
    """Run one experiment point. PDF §1–6.

    Inputs: config, experiment point (n_tasks, m, U_norm, ...), dry_run.
    Outputs: ExperimentPoint with result filled (or unchanged if dry_run).
    Invariants: seed set for reproducibility; no side effects if dry_run.
    """
    if dry_run:
        return point
    # TODO: generate task set, resources, partition, schedule; compute metrics; fill point.result
    point.result = SimulationResult(
        task_set_id="",
        feasible=True,
        core_allocation={},
        group_allocation={},
        metrics={},
    )
    return point


def run_all(
    config: Config,
    dry_run: bool = False,
    output_dir: Path | None = None,
) -> list[ExperimentPoint]:
    """Run full experiment sweep. PDF §1–6.

    Inputs: config, dry_run, optional output_dir.
    Outputs: list of ExperimentPoint with results (or empty/placeholders if dry_run).
    Invariants: validates config; creates output dirs when not dry_run.
    """
    out = Path(output_dir or config.output_dir)
    if not dry_run:
        out.mkdir(parents=True, exist_ok=True)
        config.results_dir.mkdir(parents=True, exist_ok=True)
    # TODO: sweep over n_tasks, m, U_norm, n_resources, total_accesses; run_experiment each
    points: list[ExperimentPoint] = []
    points.append(
        ExperimentPoint(
            n_tasks=config.gen.n_tasks,
            m=config.system.m_max,
            U_norm=(config.system.U_norm_min + config.system.U_norm_max) / 2,
            n_resources=config.resources.n_resources_max,
            total_resource_accesses=config.resources.total_access_options[0],
            seed=config.seed,
        )
    )
    for p in points:
        run_experiment(config, p, dry_run=dry_run)
    return points
