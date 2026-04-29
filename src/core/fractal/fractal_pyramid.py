"""Full fractal pyramid generation."""

def fractal_pyramid(max_level: int = 10):
    from .fractal_pyramid_level import fractal_pyramid_level
    return [(level, *fractal_pyramid_level(level)) for level in range(1, max_level + 1)]
