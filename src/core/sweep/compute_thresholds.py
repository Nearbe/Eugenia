"""Threshold generation for sweep processing."""


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
def compute_thresholds(sweep_min: float, sweep_max: float, sweep_step: float) -> list[float]:
    if sweep_step <= 0:
        raise ValueError("sweep_step must be positive")
    if sweep_max <= sweep_min:
        raise ValueError("sweep_max must be greater than sweep_min")

    count = int((sweep_max - sweep_min) / sweep_step) + 1
    return [sweep_min + index * sweep_step for index in range(count)]
