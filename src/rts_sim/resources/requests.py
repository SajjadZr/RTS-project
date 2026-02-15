"""Resource request generation: total accesses and per-task distribution. PDF §3–4."""

from __future__ import annotations

from rts_sim.models import DAGTask, ResourceRequest, TaskSet
from rts_sim.utils.seeds import get_rng


def generate_resource_requests(
    task_set: TaskSet,
    n_resources: int,
    total_accesses: int,
    csp_min: float = 0.1,
    csp_max: float = 1.0,
    seed: int | None = None,
) -> list[ResourceRequest]:
    """Generate resource types and total access counts per resource. PDF §3–4.

    Inputs: task_set, n_resources, total_accesses (one of 10,30,50,80,150), CSP range, seed.
    Outputs: list of ResourceRequest (resource_id, total_access_count, csp_fraction).
    Invariants: total accesses across resources ~ total_accesses; then distribute to tasks.
    """
    rng = get_rng(seed)
    # TODO: pick total_accesses from options; distribute across n_resources; assign to tasks
    requests: list[ResourceRequest] = []
    for q in range(n_resources):
        requests.append(
            ResourceRequest(
                resource_id=f"l{q+1}",
                total_access_count=max(1, total_accesses // n_resources),
                csp_fraction=(csp_min + csp_max) / 2,
            )
        )
    return requests
