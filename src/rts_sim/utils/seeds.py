"""Random seed handling for reproducibility.

PDF reference: Section 2 (task generation), Section 4 (resource allocation).
Inputs: optional seed (int).
Outputs: numpy/random RNG or seed set.
Invariants: same seed yields same task set and resource distribution.
"""

import random
from typing import Any

# TODO: use numpy.random.default_rng(seed) when implementing gen/resources

_seed: int | None = None


def set_global_seed(seed: int) -> None:
    """Set global random seed for reproducibility. PDF §2, §4."""
    global _seed
    _seed = seed
    random.seed(seed)
    # TODO: numpy.random.seed(seed) if using numpy


def get_rng(seed: int | None = None) -> Any:
    """Return a RNG instance. If seed is None, use global seed. PDF §2, §4.

    Inputs: optional seed.
    Outputs: random number generator (currently stdlib random).
    """
    s = seed if seed is not None else _seed
    if s is not None:
        random.seed(s)
    return random
    # TODO: return np.random.default_rng(s) for RandFixedSum / UUniFast
