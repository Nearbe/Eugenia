"""Visualize fractal pyramid as string."""


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
def fractal_pyramid_to_string(max_level: int = 10, width: int | None = None):
    from .fractal_pyramid import fractal_pyramid

    line_width = (max_level * 4) if width is None else width
    return "\n".join(
        f"L{level}: {left} | {center} | {right}".center(line_width)
        for level, left, center, right in fractal_pyramid(max_level)
    )
