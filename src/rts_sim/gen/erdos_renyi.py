"""Erdős–Rényi DAG generation and source/sink addition.

PDF reference: Section 2 – task generation, G(|V_i|, p), p=0.1, add source and sink.
Inputs: n_nodes (int), p (float), rng (optional).
Outputs: nodes list, edges list (with single root and single sink).
Invariants: one source (in-degree 0), one sink (out-degree 0); source/sink have zero execution.
"""

from __future__ import annotations

from rts_sim.models import Edge, Node
from rts_sim.models import Criticality
from rts_sim.utils.seeds import get_rng


def erdos_renyi_dag_with_source_sink(
    n_nodes: int,
    p: float = 0.1,
    seed: int | None = None,
) -> tuple[list[Node], list[Edge]]:
    """Build DAG via Erdős–Rényi G(n, p) and add source/sink. PDF §2.

    Inputs: n_nodes (internal nodes, excluding source/sink), p (edge probability), seed.
    Outputs: (nodes, edges) with source and sink; source/sink have c_normal=c_overflow=0.
    Invariants: graph is a DAG; single root, single leaf.
    """
    rng = get_rng(seed)
    # TODO: generate G(n_nodes, p) as DAG (only i->j for i < j or random topological order)
    # TODO: add source connected to all roots, sink connected from all leaves
    # Placeholder: minimal structure
    nodes: list[Node] = [
        Node(id="source", criticality=Criticality.LO, c_normal=0.0, c_overflow=0.0),
        Node(id="sink", criticality=Criticality.LO, c_normal=0.0, c_overflow=0.0),
    ]
    edges: list[Edge] = [Edge(src="source", dst="sink")]
    return nodes, edges
