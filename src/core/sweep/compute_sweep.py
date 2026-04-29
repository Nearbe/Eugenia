"""Core sweep computation for delta-field visualization via Eugenia core math."""

#  Copyright (c) 2026.
#  ╔═══════════════════════════════════╗
#  ║ Русский  ║ English    ║ Ελληνικά  ║
#  ║══════════║════════════║═══════════║
#  ║ Евгений  ║ Eugene     ║ Εὐγένιος  ║
#  ║ Евгения  ║ Eugenia    ║ Εὐγενία   ║
#  ║ Евгеника ║ Eugenics   ║ Εὐγενική  ║
#  ║ Евгениос ║ Eugenius   ║ Εὐγένιος  ║
#  ║ Женя     ║ Zhenya     ║ Ζένια     ║
#  ╚═══════════════════════════════════╝
from .compute_jump_events import compute_jump_events
from .compute_thresholds import compute_thresholds
from .linear_algebra import CoreMatrix, CoreVector, to_vector
from .sweep_results import SweepResults

DEFAULT_SWEEP_MIN = -5.6
DEFAULT_SWEEP_MAX = 5.6
DEFAULT_SWEEP_STEP = 0.1
DEFAULT_JUMP_THRESHOLD = 1.0
PERCENT = 100.0


def compute_sweep(data) -> SweepResults:
    sweep_min = float(getattr(data, "delta_min", DEFAULT_SWEEP_MIN))
    sweep_max = float(getattr(data, "delta_max", DEFAULT_SWEEP_MAX))
    config = getattr(data, "config", {}) or {}
    sweep_step = float(config.get("sweep_step", DEFAULT_SWEEP_STEP))
    jump_threshold = float(config.get("jump_threshold", DEFAULT_JUMP_THRESHOLD))

    thresholds = CoreVector(compute_thresholds(sweep_min, sweep_max, sweep_step))
    fields = list(getattr(data, "symbol_delta_fields", []))
    occupancy_rows: list[list[float]] = []

    for threshold in thresholds:
        row: list[float] = []
        for field in fields:
            values = to_vector(field)
            if not values:
                row.append(0.0)
                continue
            active_count = sum(1 for value in values if value >= threshold)
            row.append(float(active_count / len(values) * PERCENT))
        occupancy_rows.append(row)

    occupancy_rates = CoreMatrix(occupancy_rows)
    per_class_rates = occupancy_rates.T.tolist() if occupancy_rows else []
    jump_events, jump_count = compute_jump_events(thresholds.tolist(), per_class_rates, jump_threshold)

    return SweepResults(
        thresholds=thresholds,
        occupancy_rates=occupancy_rates,
        jump_events=jump_events,
        jump_count=jump_count,
    )
