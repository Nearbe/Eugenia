"""Fractal pyramid structure for pattern diagnostics."""


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
def fractal_pyramid_structure(values_or_levels, max_depth: int = 5) -> list[dict]:
    if isinstance(values_or_levels, int):
        values = list(range(max(values_or_levels, 0)))
        depth_limit = max(values_or_levels, 0)
    else:
        values = list(values_or_levels)
        depth_limit = max_depth

    result: list[dict] = []
    for depth in range(1, depth_limit + 1):
        size = min(max(len(values) // depth, 1), depth) if values else 1
        sample = values[:size]
        mean_value = sum(sample) / len(sample) if sample else 0.0
        result.append(
            {
                "depth": depth,
                "size": size,
                "values": sample,
                "mean": mean_value,
                "bridge_analysis": {"left_spine_level": float(depth - 1)},
            }
        )
    return result
