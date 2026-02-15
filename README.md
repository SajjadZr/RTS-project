# RTS Simulator

Mixed-criticality DAG task scheduling simulator: federated scheduling, resource management, and grouping-by-resource partitioning. Based on the specification in `docs/project_info_1404_PQ_3.pdf`.

## Requirements

- Python 3.10+
- Dependencies: `typer`, `pyyaml`, `pydantic` (see `pyproject.toml`)

## Install

```bash
pip install -e .
```

## Usage

- **CLI**
  - `python -m rts_sim --help`
  - `python -m rts_sim generate [--config config.yaml] [--output output/task_set.json]`
  - `python -m rts_sim run [--config config.yaml] [--dry-run]`
  - `python -m rts_sim plot [--config config.yaml] [--output-dir plots]`
  - `python -m rts_sim all [--dry-run]` — full pipeline (generate → run → plot); `--dry-run` validates config and creates folders only.

- **Config**  
  YAML/JSON config with defaults matching the PDF (see `config.yaml`). Options: `system` (m, U_norm), `gen` (n_tasks, DAG params), `resources`, `partition`, `sched`, `seed`, `output_dir`, `results_dir`, `plots_dir`.

## Layout

- `src/rts_sim/` — main package  
  - `gen/` — task-set and DAG generation (Erdős–Rényi, UUniFast, RandFixedSum)  
  - `resources/` — resource request generation and normal/critical segments  
  - `partition/` — federated scheduling and grouping-by-resource  
  - `sched/` — CA-EDF and suspension-based FIFO lock (HI/LO)  
  - `experiments/` — runner, metrics, reproducibility  
  - `analysis/` — plots and aggregations  
  - `utils/` — seeds, logging, types  
- `config.yaml` — default config  
- `SPEC.md` — specification summary  
- `tests/` — unit tests

## Tests

```bash
pytest tests/ -v
```

## Status

Skeleton only: CLI, config, data models, and placeholders for all algorithms. No full logic or plots yet.
