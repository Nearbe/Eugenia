from __future__ import annotations

from typing import Mapping

from ..algebra import compress

POTENTIAL_PREIMAGE_WEIGHT = 0.0


def invariant_measure_holds(
    measure: Mapping[object, float],
    preimage: Mapping[object, tuple[object, ...]],
    event: object,
) -> bool:
    """Return true when ``μ(D⁻¹(A)) = μ(A)`` for a finite partition.

    ``D`` doubles states, so each point of the inverse image contributes through
    the inverse branch ``H``. The preimage mass is therefore compressed once.
    """
    event_measure = float(measure.get(event, 0.0))
    preimage_mass = sum(float(measure.get(state, 0.0)) for state in preimage.get(event, ()))
    if preimage_mass == POTENTIAL_PREIMAGE_WEIGHT:
        return event_measure == POTENTIAL_PREIMAGE_WEIGHT
    preimage_measure = float(compress(preimage_mass))
    return preimage_measure == event_measure
