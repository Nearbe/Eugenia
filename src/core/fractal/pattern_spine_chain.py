"""Build a compact Ω → Π spine chain for values."""

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
from .L import L
from .spine_value import spine_value


def pattern_spine_chain(values) -> list[dict]:
    if isinstance(values, int):
        iterable = range(max(values, 0))
    elif isinstance(values, float):
        iterable = [values]
    else:
        iterable = values

    return [
        {"index": index, "value": float(value), "spine_level": L(float(value)), "spine": spine_value(L(float(value)))}
        for index, value in enumerate(iterable)
    ]
