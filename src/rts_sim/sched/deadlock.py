"""Deadlock detection and dropping low-criticality in overload. PDF §6."""

from __future__ import annotations

from rts_sim.models import TaskSet


def deadlock_detect(
    task_set: TaskSet,
    resource_hold: dict[str, str],  # task_id -> resource_id
    resource_wait: dict[str, str],  # task_id -> resource_id
) -> bool:
    """Detect deadlock (cycle in resource wait graph). PDF §6.

    Inputs: task_set, who holds which resource, who waits for which resource.
    Outputs: True if deadlock detected.
    Invariants: non-nested; one resource per task at a time.
    """
    # TODO: build wait graph; detect cycle
    return False


def drop_low_criticality_in_overload(
    task_set: TaskSet,
    overload_flag: bool,
) -> TaskSet:
    """In overload, drop LO-criticality DAGs to recover. PDF §6.

    Inputs: task_set, whether system is in overload.
    Outputs: possibly reduced TaskSet (only HI tasks if overload).
    Invariants: only drop when overload; prefer HI tasks.
    """
    # TODO: if overload, filter to HI-only tasks (e.g. by graph criticality)
    if not overload_flag:
        return task_set
    # Placeholder: return as-is
    return task_set
