"""Fractal volume scaling."""
def fractal_volume_scaling(binary_masks, thresholds):
    return [{"mask": i, "volumes": [{"threshold": t, "volume": sum(1 for row in m for v in row if v > t)} for t in thresholds]} for i, m in enumerate(binary_masks)]
