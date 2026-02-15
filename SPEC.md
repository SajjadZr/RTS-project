# Specification Summary (from PDF)

Reference: `docs/project_info_1404_PQ_3.pdf` — mixed-criticality DAG tasks, two-priority lock, two partitioning approaches.

## 1. Initial system setup

- **m** (processors): \(m = \lceil U_\sum / U_{norm} \rceil\); \(m \in [2, 64]\).
- **U_norm** (normalized utilization): total utilization / m; \(U_{norm} \in [0.1, 1]\).
- **U_sum**: \(m \cdot U_{norm}\).
- **Task utilizations**: RandFixedSum over \(n\) tasks so that \(\sum u_i = U_\sum\); each \(u_i\) can be \(> 1\) or \(< 1\).
- **Modes**: normal and overflow; in overflow, nodes use overflow WCET.

## 2. Task generation

- Each task \(\tau_i\) is a DAG.
- **DAG**: Erdős–Rényi \(G(|V_i|, p)\), \(p = 0.1\); then add **source** and **sink** (single root, single leaf); source/sink have zero execution.
- **|V_i|**: random in \([20, 50]\).
- **Node criticality**: 50% HI, 50% LO.
- **Node utilization (overflow)**: UUniFast over nodes, each \(< 1\); normal \(\le\) overflow.
- **Period \(T_i\)**: random from \(\{2000, 4000, 6000\}\); **\(D_i = T_i\)**.
- **WCET**: \(c(\nu_{i,k}) = u_{i,k} \cdot T_i\) (normal and overflow).
- **\(C_i\)**: sum of node WCETs; **\(L_i\)**: critical path length (longest path) in normal and overflow.

## 3. Resources

- **\(n_r\)** shared resources \(\Theta = \{l_1, \ldots, l_{n_r}\}\); \(n_r \in [2, 8]\).
- Each task can request shared resources; access is **exclusive** and **non-nested**.

## 4. Resource allocation to tasks

- Each node \(\nu\) is a sequence of **normal** and **critical** segments: \(\nu = \{c_{i,1}, c'_{i,1}, \ldots, c'_{i,s-1}, c_{i,s}\}\).
- **Total accesses** (over all tasks): one of \(\{10, 30, 50, 80, 150\}\); distribute across resources and tasks.
- **CSP**: critical segment length as fraction of node WCET in \([0.1, 1]\); RandFixedSum for splitting.
- Remainder of node execution is normal; order normal/critical/normal/... is fixed.

## 5. Federated scheduling

- **Heavy** (\(U_i > 1\)): \(m_i = \lceil (C_i - L_i) / (D_i - L_i) \rceil\) cores, exclusive.
- **Light** (\(U_i \le 1\)): one core each, exclusive.
- Total cores used must \(\le m\); else task set infeasible.
- **WFD** (Worst-Fit Decreasing): place light tasks on remaining cores.

## 6. Grouping by most-requested resource

- For each resource type, form a **group** of tasks that have **maximum** accesses to that resource (each task in exactly one group).
- Sort groups by **total utilization (overflow)** descending.
- Allocate \(m_{group} = \lceil U_\sum \rceil\) cores per group (exclusive); remaining tasks go to remaining cores.
- If not enough cores, assign group to the set of cores with most remaining capacity.

## Scheduling and lock protocol

- **CA-EDF**: Criticality-Aware EDF.
- **Lock protocol**: suspension-based FIFO with **two priority queues (HI/LO)** per resource.
- **Deadlock**: detect and, in overload, **drop low-criticality** (e.g. drop LO DAGs).

## Repo mapping

| PDF section | Repo |
|-------------|------|
| §1 | `config.py` (system), `gen/utilization.py` (RandFixedSum) |
| §2 | `gen/` (Erdős–Rényi, source/sink, UUniFast, periods, \(C_i\), \(L_i\)) |
| §3–4 | `resources/` (requests, segments) |
| §5 | `partition/federated.py` (federated, WFD) |
| §6 | `partition/grouping.py`, `sched/lock.py`, `sched/deadlock.py` |
| Experiments | `experiments/`, `analysis/` |
