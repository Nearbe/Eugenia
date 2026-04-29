"""RG-aware sweep thresholds."""
def rg_aware_sweep(sweep_min, sweep_max, n_levels=160000):
    return sorted(set(t for level in range(n_levels) for k in range(-4, 5) if sweep_min <= (t := sweep_min + (sweep_max - sweep_min) * level / n_levels + k * (2.0 ** (-level))) <= sweep_max))
