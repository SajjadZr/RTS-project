"""Grouping by most-requested resource. PDF §6."""

from __future__ import annotations

from rts_sim.models import DAGTask, TaskSet


def grouping_by_most_requested_resource(
    task_set: TaskSet,
    resource_request_counts: dict[str, dict[str, int]],  # task_id -> resource_id -> count
    n_resources: int,
) -> list[list[str]]:
    """Group tasks by resource they access most. PDF §6.

    Inputs: task_set, per-task per-resource access counts, n_resources.
    Outputs: list of groups (each group = list of task_ids); sorted by group utilization descending.
    Invariants: each task in exactly one group; groups ordered by total utilization (overflow).
    """
    # TODO: for each task find argmax resource; put task in that group; sort groups by U_sum
    groups: list[list[str]] = [[] for _ in range(n_resources)]
    for t in task_set.tasks:
        counts = resource_request_counts.get(t.task_id, {})
        if not counts:
            groups[0].append(t.task_id)
            continue
        best = max(counts, key=counts.get)  # type: ignore
        idx = int(best.replace("l", "")) - 1 if best.startswith("l") else 0
        idx = max(0, min(idx, n_resources - 1))
        groups[idx].append(t.task_id)
    return [g for g in groups if g]
