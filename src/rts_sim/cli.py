"""CLI via Typer: generate, run, plot, all. PDF §1–6."""

from __future__ import annotations

from pathlib import Path

import typer
from rts_sim import __version__
from rts_sim.config import load_config, resolve_config_path
from rts_sim.experiments.runner import run_all
from rts_sim.gen.dag import generate_dag_task_set
from rts_sim.analysis.plots import plot_results
from rts_sim.analysis.aggregate import aggregate_results
from rts_sim.utils.logging import setup_logging

app = typer.Typer(
    name="rts-sim",
    help="RTS simulation: mixed-criticality DAG tasks, federated scheduling, resource management.",
    add_completion=False,
)


def _get_config(config_path: str | None) -> "Config":
    from rts_sim.config import Config

    path = resolve_config_path(config_path)
    return load_config(path)


@app.command()
def generate(
    config_path: str | None = typer.Option(None, "--config", "-c"),
    output: Path = typer.Option(Path("output/task_set.json"), "--output", "-o"),
    seed: int | None = typer.Option(None, "--seed", "-s"),
) -> None:
    """Generate task set and DAGs (PDF §2). Writes task set to --output."""
    cfg = _get_config(config_path)
    if seed is not None:
        cfg.seed = seed
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    ts = generate_dag_task_set(cfg, seed=cfg.seed, output_path=output)
    typer.echo(f"Generated {len(ts.tasks)} tasks -> {output}")


@app.command()
def run(
    config_path: str | None = typer.Option(None, "--config", "-c"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Validate config and create dirs only"),
    output_dir: Path | None = typer.Option(None, "--output-dir", "-o"),
) -> None:
    """Run experiments (PDF §5–6). Use --dry-run to skip simulation."""
    cfg = _get_config(config_path)
    out = Path(output_dir) if output_dir else cfg.output_dir
    if dry_run:
        out.mkdir(parents=True, exist_ok=True)
        cfg.results_dir.mkdir(parents=True, exist_ok=True)
        typer.echo("Dry run: config validated, output dirs created.")
        return
    points = run_all(cfg, dry_run=False, output_dir=out)
    typer.echo(f"Ran {len(points)} experiment point(s).")


@app.command()
def plot(
    config_path: str | None = typer.Option(None, "--config", "-c"),
    results_dir: Path | None = typer.Option(None, "--results-dir"),
    output_dir: Path | None = typer.Option(None, "--output-dir", "-o"),
) -> None:
    """Generate plots from results (PDF §1–6). Placeholder: no plots yet."""
    cfg = _get_config(config_path)
    res_dir = Path(results_dir) if results_dir else cfg.results_dir
    out_dir = Path(output_dir) if output_dir else cfg.plots_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    # TODO: load experiment points from results_dir; call plot_results
    plot_results([], out_dir)
    typer.echo(f"Plots dir ready: {out_dir} (no plot files yet).")


@app.command()
def all(
    config_path: str | None = typer.Option(None, "--config", "-c"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Validate configs and create folders only"),
    output_dir: Path | None = typer.Option(None, "--output-dir", "-o"),
) -> None:
    """Run full pipeline: generate -> run -> plot. Use --dry-run to validate only."""
    cfg = _get_config(config_path)
    out = Path(output_dir) if output_dir else cfg.output_dir
    out.mkdir(parents=True, exist_ok=True)
    cfg.results_dir.mkdir(parents=True, exist_ok=True)
    cfg.plots_dir.mkdir(parents=True, exist_ok=True)
    if dry_run:
        typer.echo("Dry run: config validated, output/results/plots dirs created.")
        return
    # Generate
    ts = generate_dag_task_set(cfg, output_path=out / "task_set.json")
    # Run
    points = run_all(cfg, dry_run=False, output_dir=out)
    # Aggregate + plot
    aggregate_results(points, output_path=cfg.results_dir / "aggregate.csv")
    plot_results(points, cfg.plots_dir)
    typer.echo("Pipeline complete.")


@app.callback()
def global_options(
    version: bool = typer.Option(False, "--version", "-V", help="Show version", is_eager=True),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose logging"),
) -> None:
    if version:
        typer.echo(__version__)
        raise typer.Exit(0)
    level = __import__("logging").DEBUG if verbose else __import__("logging").INFO
    setup_logging(level=level)


if __name__ == "__main__":
    app()
