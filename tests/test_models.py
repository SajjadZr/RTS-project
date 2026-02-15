"""Data model tests."""

import pytest

from rts_sim.models import (
    Criticality,
    DAGTask,
    Edge,
    Node,
    Segment,
    TaskSet,
    SimulationResult,
    ExperimentPoint,
    ResourceRequest,
)


def test_node_creation() -> None:
    """Node has id, criticality, c_normal, c_overflow."""
    n = Node(id="v1", criticality=Criticality.HI, c_normal=10.0, c_overflow=12.0)
    assert n.id == "v1"
    assert n.c_normal == 10.0
    assert n.total_length_normal() == 10.0


def test_edge_creation() -> None:
    """Edge has src and dst."""
    e = Edge(src="a", dst="b")
    assert e.src == "a" and e.dst == "b"


def test_dag_task_heavy_light() -> None:
    """Heavy task has U > 1."""
    heavy = DAGTask(task_id="t1", T=100.0, D=100.0, U_overflow=1.5, U_normal=1.2, C_normal=120, C_overflow=150, L_normal=50, L_overflow=60)
    light = DAGTask(task_id="t2", T=100.0, D=100.0, U_overflow=0.5, U_normal=0.4, C_normal=40, C_overflow=50, L_normal=20, L_overflow=25)
    assert heavy.is_heavy() is True
    assert light.is_heavy() is False


def test_task_set_U_sum() -> None:
    """TaskSet.U_sum is sum of task utilizations."""
    ts = TaskSet(tasks=[
        DAGTask(task_id="a", T=10, D=10, U_overflow=0.5, U_normal=0.4, C_normal=4, C_overflow=5, L_normal=2, L_overflow=2.5),
        DAGTask(task_id="b", T=10, D=10, U_overflow=0.3, U_normal=0.3, C_normal=3, C_overflow=3, L_normal=1, L_overflow=1),
    ])
    assert ts.U_sum == 0.8


def test_simulation_result_serializable() -> None:
    """SimulationResult can be dict/json."""
    r = SimulationResult(task_set_id="x", feasible=True, core_allocation={"t1": 2}, metrics={"U": 0.9})
    d = r.model_dump()
    assert d["feasible"] is True
    assert d["core_allocation"]["t1"] == 2


def test_experiment_point_bounds() -> None:
    """ExperimentPoint validates m and U_norm ranges."""
    p = ExperimentPoint(n_tasks=10, m=8, U_norm=0.5, n_resources=4, total_resource_accesses=30)
    assert p.m >= 2 and p.m <= 64
    assert p.U_norm >= 0.1 and p.U_norm <= 1.0
