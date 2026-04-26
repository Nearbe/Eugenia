"""Fractal pyramid level: (left, center, right)."""

def fractal_pyramid_level(n):
    return (" ".join(str(n - i) for i in range(1, n)) if n > 1 else "", "0", " ".join(str(i) for i in range(1, n)) if n > 1 else "")
