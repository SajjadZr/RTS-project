"""Federated scheduling: core allocation m_i = ceil((C-L)/(D-L)), WFD. PDF §5."""

from __future__ import annotations

import math

from rts_sim.models import DAGTask, TaskSet


def federated_core_allocation(
    task_set: TaskSet,
    m_total: int,
) -> dict[str, int]:
    """Allocate cores to tasks: heavy get m_i = ceil((C_i - L_i)/(D_i - L_i)), light get 1. PDF §5.

    Inputs: task_set, total number of processors m.
    Outputs: dict task_id -> m_i (cores). Infeasible if sum m_i > m.
    Invariants: heavy (U_i > 1) get m_i cores; light get 1; sum m_i <= m for feasibility.
    """
    # TODO: for each task compute m_i; check sum <= m
    alloc: dict[str, int] = {}
    for t in task_set.tasks:
        if t.is_heavy():
            # m_i = ceil((C_i - L_i) / (D_i - L_i))
            denom = t.D - t.L_overflow
            num = t.C_overflow - t.L_overflow
            m_i = max(1, math.ceil(num / denom)) if denom > 0 else 1
        else:
            m_i = 1
        alloc[t.task_id] = m_i
    return alloc


def wfd_placement(
    task_set: TaskSet,
    core_allocation: dict[str, int],
    m_total: int,
) -> dict[int, list[str]]:
    """Worst-Fit Decreasing: place light tasks on remaining cores. PDF §5.

    Inputs: task_set, core_allocation (task_id -> m_i), m_total.
    Outputs: core_id -> list of task_ids assigned to that core (for light tasks).
    Invariants: heavy tasks already have exclusive cores; light tasks fill remaining.
    """
    # TODO: sort light tasks by utilization decreasing; assign to core with least used capacity
    used = sum(core_allocation.get(t.task_id, 1) for t in task_set.tasks)
    remaining = max(0, m_total - used)
    return {c: [] for c in range(remaining)}
