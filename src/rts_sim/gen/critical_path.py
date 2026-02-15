"""Critical path computation for DAG tasks. PDF §2."""

from __future__ import annotations

from rts_sim.models import DAGTask, Edge, Node


def critical_path_length(
    nodes: list[Node],
    edges: list[Edge],
    node_lengths: dict[str, float],
) -> float:
    """Longest path length in DAG. PDF §2 – L_i = max path len over π in G_i.

    Inputs: nodes, edges, node_lengths (node_id -> execution time).
    Outputs: length of longest path (sum of node_lengths along path).
    Invariants: graph is a DAG; source/sink have length 0.
    """
    # TODO: topological sort + dynamic programming (longest path)
    if not nodes:
        return 0.0
    return max(node_lengths.get(n.id, 0.0) for n in nodes)
