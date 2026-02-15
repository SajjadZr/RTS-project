"""Aggregate experiment results. PDF §1–6."""

from __future__ import annotations

from pathlib import Path

from rts_sim.models import ExperimentPoint


def aggregate_results(
    points: list[ExperimentPoint],
    output_path: Path | None = None,
) -> dict[str, float]:
    """Aggregate metrics across experiment points. PDF §1–6.

    Inputs: list of ExperimentPoint, optional output_path to write CSV/JSON.
    Outputs: dict of aggregated metric name -> value.
    Invariants: deterministic; optional file write.
    """
    # TODO: mean feasibility, std, etc.; write CSV if output_path set
    if not points:
        return {}
    feasible = sum(1 for p in points if p.result and p.result.feasible)
    out = {"feasibility_ratio": feasible / len(points), "n_points": len(points)}
    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"feasibility_ratio,{out['feasibility_ratio']}\nn_points,{out['n_points']}\n")
    return out
