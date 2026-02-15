"""UUniFast and RandFixedSum utilization generation.

PDF reference: Section 1 (RandFixedSum for task util), Section 2 (UUniFast for node util).
Inputs: n (number of values), U_sum (total utilization), rng/seed.
Outputs: list of n utilizations summing to U_sum (RandFixedSum) or with expected mean (UUniFast).
Invariants: each u_i in (0,1) for UUniFast; sum(u_i)=U_sum for RandFixedSum.
"""

from __future__ import annotations


def rand_fixed_sum(
    n: int,
    U_sum: float,
    seed: int | None = None,
) -> list[float]:
    """Generate n utilization values that sum to U_sum. PDF §1.

    Inputs: n (number of tasks), U_sum (total utilization), seed.
    Outputs: [u_1, ..., u_n] with sum equal to U_sum.
    Invariants: each u_i >= 0; sum(u_i) = U_sum (within float precision).
    """
    # TODO: implement RandFixedSum (rejection or Dirichlet-based)
    # Placeholder: equal split
    if n <= 0:
        return []
    u = U_sum / n
    return [u] * n


def uunifast_discard(
    n: int,
    U_sum: float,
    seed: int | None = None,
) -> list[float]:
    """Generate n node utilizations with UUniFast discard. PDF §2.

    Inputs: n (number of nodes), U_sum (task utilization), seed.
    Outputs: [u_1, ..., u_n] each < 1, sum <= U_sum; discard if any >= 1 and retry.
    Invariants: each u_i in (0, 1); used for overflow mode; normal <= overflow per node.
    """
    # TODO: implement UUniFast discard (random breakdown of U_sum, reject if any >= 1)
    # Placeholder: equal split, capped
    if n <= 0:
        return []
    u = min(U_sum / n, 0.99)
    return [u] * n
