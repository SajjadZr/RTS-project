"""DAG task set generation: combine ER DAG + utilization + periods. PDF §2."""

from __future__ import annotations

from pathlib import Path

from rts_sim.config import Config
from rts_sim.gen.erdos_renyi import erdos_renyi_dag_with_source_sink
from rts_sim.gen.utilization import rand_fixed_sum, uunifast_discard
from rts_sim.models import DAGTask, TaskSet
from rts_sim.utils.seeds import get_rng, set_global_seed


def generate_dag_task_set(
    config: Config,
    seed: int | None = None,
    output_path: Path | None = None,
) -> TaskSet:
    """Generate a full task set: DAGs + U_i + T_i + C_i, L_i. PDF §2.

    Inputs: config (gen + system), optional seed, optional output_path to write JSON.
    Outputs: TaskSet with DAGTask list; each task has C_normal, C_overflow, L_normal, L_overflow.
    Invariants: D_i = T_i; 50% HI / 50% LO nodes; periods in {2000, 4000, 6000}.
    """
    s = seed if seed is not None else config.seed
    set_global_seed(s)
    rng = get_rng(s)
    g = config.gen
    m = config.system.m_max  # TODO: derive m from U_norm and n_tasks
    U_norm = (config.system.U_norm_min + config.system.U_norm_max) / 2
    U_sum = m * U_norm
    # TODO: RandFixedSum for task utilizations
    u_list = rand_fixed_sum(g.n_tasks, U_sum, seed=s)
    tasks: list[DAGTask] = []
    for i, U_i in enumerate(u_list):
        # TODO: n_nodes = random in [nodes_per_task_min, nodes_per_task_max]
        n_nodes = g.nodes_per_task_min
        nodes, edges = erdos_renyi_dag_with_source_sink(
            n_nodes, g.erdos_renyi_p, seed=rng.randint(0, 2**31 - 1)
        )
        # TODO: UUniFast for node utils (overflow); normal <= overflow
        node_utils = uunifast_discard(len(nodes), U_i, seed=rng.randint(0, 2**31 - 1))
        # TODO: T_i from period_values; D_i = T_i; c(v) = u * T per node; C_i = sum c; L_i = critical path
        T = float(rng.choice(g.period_values))
        C_normal = C_overflow = 0.0
        for j, node in enumerate(nodes):
            u_node = node_utils[j] if j < len(node_utils) else 0.0
            # Placeholder: we don't mutate Node; would need to build new nodes with c_normal, c_overflow
            C_overflow += u_node * T
        C_normal = C_overflow * 0.8  # placeholder
        L_normal = C_normal  # TODO: critical path
        L_overflow = C_overflow
        tasks.append(
            DAGTask(
                task_id=f"tau_{i}",
                nodes=nodes,
                edges=edges,
                T=T,
                D=T,
                U_normal=U_i * 0.8,
                U_overflow=U_i,
                C_normal=C_normal,
                C_overflow=C_overflow,
                L_normal=L_normal,
                L_overflow=L_overflow,
            )
        )
    ts = TaskSet(tasks=tasks)
    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ts.model_dump_json(indent=2))
    return ts
