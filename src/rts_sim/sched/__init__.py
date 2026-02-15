"""Baseline EDF/CA-EDF and lock protocol simulation. PDF §5–6."""

from rts_sim.sched.ca_edf import ca_edf_schedule
from rts_sim.sched.lock import suspension_fifo_lock_hi_lo
from rts_sim.sched.deadlock import deadlock_detect, drop_low_criticality_in_overload

__all__ = [
    "ca_edf_schedule",
    "suspension_fifo_lock_hi_lo",
    "deadlock_detect",
    "drop_low_criticality_in_overload",
]
