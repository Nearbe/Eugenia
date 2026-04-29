"""Count connected components."""

def count_components(mask):
    from .label_2d import label_2d
    labeled = label_2d(mask)
    return len({v for row in labeled for v in row if v > 0})
