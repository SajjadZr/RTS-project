"""Federated scheduling and grouping-by-resource partitioning. PDF §5–6."""

from rts_sim.partition.federated import federated_core_allocation, wfd_placement
from rts_sim.partition.grouping import grouping_by_most_requested_resource

__all__ = [
    "federated_core_allocation",
    "wfd_placement",
    "grouping_by_most_requested_resource",
]
