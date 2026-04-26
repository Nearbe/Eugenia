"""Visualize fractal pyramid as string."""

def fractal_pyramid_to_string(max_level: int = 10, width: int | None = None):
    from .fractal_pyramid import fractal_pyramid
    w = (max_level * 4) if width is None else width
    return "\n".join(f"L{l}: {le} | {c} | {ri}".center(w) for l, le, c, ri in fractal_pyramid(max_level))
