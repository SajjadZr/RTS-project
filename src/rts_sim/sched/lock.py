"""Suspension-based FIFO lock with two priority queues (HI/LO). PDF §6."""

from __future__ import annotations

from rts_sim.models import Criticality


def suspension_fifo_lock_hi_lo(
    requests: list[tuple[str, str, Criticality]],  # (task_id, resource_id, criticality)
) -> list[tuple[str, str, float, float]]:
    """Simulate FIFO lock with HI/LO queues per resource. PDF §6.

    Inputs: list of (task_id, resource_id, criticality) request events.
    Outputs: list of (task_id, resource_id, acquire_time, release_time) or similar.
    Invariants: non-nested access; FIFO within HI and within LO; HI has priority over LO.
    """
    # TODO: two queues per resource (HI, LO); serve HI first, then LO FIFO; suspension during wait
    return []
