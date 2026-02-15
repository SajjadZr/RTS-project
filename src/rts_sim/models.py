"""Data models for RTS simulation.

PDF reference: Sections 1–6 (docs/project_info_1404_PQ_3.pdf).
Invariants: D_i = T_i; segments are non-nested; critical path L_i defined per mode.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Criticality(str, Enum):
    """Per-node/task criticality level. PDF §2."""

    HI = "hi"
    LO = "lo"


class ResourceType(str, Enum):
    """Shared resource identifier. PDF §3. Concrete resources l1, l2, ... from config."""

    L1 = "l1"
    L2 = "l2"
    # Extend with l3, l4, ... as needed per n_resources


class Node(BaseModel):
    """A vertex in a DAG task. PDF §2.

    Inputs: id, criticality, execution times (normal/overflow), optional segments.
    Outputs: immutable node representation.
    Invariants: source/sink have execution 0; 50% HI / 50% LO (over task set).
    """

    id: str
    criticality: Criticality = Criticality.LO
    c_normal: float = Field(ge=0, description="WCET in normal mode")
    c_overflow: float = Field(ge=0, description="WCET in overflow mode")
    segments: list["Segment"] = Field(default_factory=list)
    model_config = {"frozen": True}

    def total_length_normal(self) -> float:
        """Sum of execution in normal mode (for critical path)."""
        # TODO: add segment lengths in normal mode
        return self.c_normal

    def total_length_overflow(self) -> float:
        """Sum of execution in overflow mode."""
        # TODO: add segment lengths in overflow mode
        return self.c_overflow


class Edge(BaseModel):
    """Directed edge (precedence) in a DAG. PDF §2.

    Inputs: source node id, destination node id.
    Outputs: immutable edge.
    Invariants: no self-loops; DAG has single source and single sink after gen.
    """

    src: str
    dst: str
    model_config = {"frozen": True}


class Segment(BaseModel):
    """A normal or critical execution segment within a node. PDF §4.

    Inputs: kind (normal/critical), duration(s), optional resource id.
    Outputs: segment representation.
    Invariants: sequence per node is normal, critical, normal, ...; non-nested access.
    """

    class Kind(str, Enum):
        NORMAL = "normal"
        CRITICAL = "critical"

    kind: Kind
    length_normal: float = Field(ge=0)
    length_overflow: float = Field(ge=0)
    resource_id: str | None = None  # for critical segments
    model_config = {"frozen": True}


class ResourceRequest(BaseModel):
    """Request for a shared resource (count and per-node distribution). PDF §3–4.

    Inputs: resource_id, total_access_count, CSP fraction.
    Outputs: request record for allocation.
    """

    resource_id: str
    total_access_count: int = Field(ge=0)
    csp_fraction: float = Field(ge=0, le=1)
    model_config = {"frozen": True}


class DAGTask(BaseModel):
    """Single DAG task τ_i. PDF §2.

    Inputs: task_id, nodes, edges, period T_i, utilization U_i (optional).
    Outputs: DAG with T_i = D_i, C_i = sum of node WCETs, L_i = critical path length.
    Invariants: one source, one sink; C_i and L_i defined for normal and overflow.
    """

    task_id: str
    nodes: list[Node] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)
    T: float = Field(gt=0)
    D: float = Field(gt=0)
    U_normal: float = Field(ge=0)
    U_overflow: float = Field(ge=0)
    C_normal: float = Field(ge=0)
    C_overflow: float = Field(ge=0)
    L_normal: float = Field(ge=0)
    L_overflow: float = Field(ge=0)
    model_config = {"frozen": False}

    @property
    def U(self) -> float:
        """Utilization (overflow mode for scheduling). PDF §2."""
        return self.U_overflow

    def is_heavy(self) -> bool:
        """True if U_i > 1 (federated: exclusive cores). PDF §5."""
        return self.U > 1.0


class TaskSet(BaseModel):
    """Set of DAG tasks T. PDF §1–2.

    Inputs: list of DAGTask.
    Outputs: task set with aggregate utilization.
    Invariants: U_sum = sum U_i; m = ceil(U_sum / U_norm) from config.
    """

    tasks: list[DAGTask] = Field(default_factory=list)

    @property
    def U_sum(self) -> float:
        """Total utilization (overflow). PDF §1."""
        return sum(t.U for t in self.tasks)


class SimulationResult(BaseModel):
    """Result of one scheduling simulation run. PDF §5–6.

    Inputs: task_set_id, partition/schedule decisions, feasibility, metrics.
    Outputs: serializable result for experiments.
    """

    task_set_id: str = ""
    feasible: bool = False
    core_allocation: dict[str, Any] = Field(default_factory=dict)
    group_allocation: dict[str, Any] = Field(default_factory=dict)
    metrics: dict[str, float] = Field(default_factory=dict)
    model_config = {"extra": "allow"}


class ExperimentPoint(BaseModel):
    """Single experiment configuration point. PDF §1–6.

    Inputs: n_tasks, m, U_norm, n_resources, etc.
    Outputs: one row for sweep / reproducibility.
    """

    n_tasks: int = Field(ge=1)
    m: int = Field(ge=2, le=64)
    U_norm: float = Field(ge=0.1, le=1.0)
    n_resources: int = Field(ge=2, le=8)
    total_resource_accesses: int = Field(ge=0)
    seed: int = 0
    result: SimulationResult | None = None
    model_config = {"extra": "allow"}


# Forward refs
Node.model_rebuild()
