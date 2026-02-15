"""Plotting (placeholder). PDF §1–6. Do NOT produce plots yet."""

from __future__ import annotations

from pathlib import Path

from rts_sim.models import ExperimentPoint


def plot_results(
    points: list[ExperimentPoint],
    output_dir: Path,
) -> None:
    """Generate plots from experiment points. PDF §1–6.

    Inputs: list of ExperimentPoint, output directory.
    Outputs: None. Do NOT produce plots in this step (placeholder).
    Invariants: creates output_dir if needed; no plot files written yet.
    """
    # TODO: plots (schedulability vs U_norm, vs n_resources, etc.)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
