"""Jump event detection for sweep occupancy rates."""


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
def compute_jump_events(
    thresholds: list[float],
    occupancy_rates: list[list[float]],
    jump_threshold: float,
) -> tuple[list[tuple[float, int, float, float, float]], int]:
    jump_events: list[tuple[float, int, float, float, float]] = []
    if not thresholds or not occupancy_rates:
        return jump_events, 0

    for class_id, rates in enumerate(occupancy_rates):
        for threshold_idx in range(min(len(thresholds), len(rates)) - 1):
            before = float(rates[threshold_idx])
            after = float(rates[threshold_idx + 1])
            change = abs(after - before)
            if change > jump_threshold:
                jump_events.append(
                    (round(float(thresholds[threshold_idx + 1]), 4), class_id, before, after, change)
                )
    return jump_events, len(jump_events)
