"""Fractal bridge analysis."""
from .constants import D_ID

def fractal_bridge_analysis(pyr_level):
    lv = [D_ID ** (pyr_level - i) for i in range(1, pyr_level)]
    rv = [D_ID ** i for i in range(1, pyr_level)]
    return {"level": pyr_level, "left_sum": sum(lv), "right_sum": sum(rv), "center": 0.0, "bridge_ratio": sum(lv) / sum(rv) if sum(rv) != 0 else float("inf")}
