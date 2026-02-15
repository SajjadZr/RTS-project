"""Assign normal/critical segments to nodes. PDF §4."""

from __future__ import annotations

from rts_sim.models import Node, Segment
from rts_sim.utils.seeds import get_rng


def assign_segments_to_nodes(
    nodes: list[Node],
    resource_assignments: dict[str, list[str]],  # node_id -> [resource_id, ...]
    csp_fraction: float,
    seed: int | None = None,
) -> list[Node]:
    """Build segment sequence per node: normal, critical, normal, ... PDF §4.

    Inputs: nodes, which node gets which resources, CSP fraction, seed.
    Outputs: new list of Node with segments filled (c_normal/c_overflow include segment lengths).
    Invariants: non-nested access; critical segment length = CSP% of node WCET; RandFixedSum for split.
    """
    rng = get_rng(seed)
    # TODO: for each node, build segments; critical segments use RandFixedSum for lengths
    out: list[Node] = []
    for n in nodes:
        segs: list[Segment] = []
        # Placeholder: one normal segment
        segs.append(
            Segment(kind=Segment.Kind.NORMAL, length_normal=n.c_normal, length_overflow=n.c_overflow)
        )
        out.append(
            Node(
                id=n.id,
                criticality=n.criticality,
                c_normal=n.c_normal,
                c_overflow=n.c_overflow,
                segments=segs,
            )
        )
    return out
