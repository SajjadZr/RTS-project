"""Metrics for experiments. PDF §5–6."""

from __future__ import annotations

from rts_sim.models import SimulationResult, TaskSet


def compute_metrics(
    task_set: TaskSet,
    result: SimulationResult,
) -> dict[str, float]:
    """Compute experiment metrics from task set and result. PDF §5–6.

    Inputs: task_set, simulation result.
    Outputs: dict of metric name -> value (e.g. schedulability, utilization, etc.).
    Invariants: deterministic given inputs.
    """
    # TODO: feasibility ratio, total utilization, per-core util, etc.
    return {
        "feasible": 1.0 if result.feasible else 0.0,
        "U_sum": task_set.U_sum,
    }
