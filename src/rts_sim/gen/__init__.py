"""Task-set and DAG generation. PDF §2."""

from rts_sim.gen.dag import generate_dag_task_set
from rts_sim.gen.erdos_renyi import erdos_renyi_dag_with_source_sink
from rts_sim.gen.utilization import uunifast_discard, rand_fixed_sum

__all__ = [
    "generate_dag_task_set",
    "erdos_renyi_dag_with_source_sink",
    "uunifast_discard",
    "rand_fixed_sum",
]
