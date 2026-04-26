"""Process class for sweep."""
def sweep_process_class(cid, symbol_delta_fields, sweep_min, sweep_max, num_thresholds, jump_threshold):
    symbol = symbol_delta_fields[cid]
    n_pixels = len(symbol)
    bin_width = (sweep_max - sweep_min) / num_thresholds
    histogram = [0.0] * num_thresholds
    for val in symbol:
        idx = int((val - sweep_min) / bin_width)
        histogram[idx if 0 <= idx < num_thresholds else num_thresholds - 1] += 1
    cumulative = [0.0] * num_thresholds
    running = 0.0
    for i in range(num_thresholds - 1, -1, -1):
        running += histogram[i]
        cumulative[i] = running
    return cid, [c / n_pixels * 100.0 if n_pixels > 0 else 0.0 for c in cumulative]
