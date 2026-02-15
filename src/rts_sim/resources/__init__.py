"""Resource request generation and critical/normal segments. PDF §3–4."""

from rts_sim.resources.requests import generate_resource_requests
from rts_sim.resources.segments import assign_segments_to_nodes

__all__ = ["generate_resource_requests", "assign_segments_to_nodes"]
