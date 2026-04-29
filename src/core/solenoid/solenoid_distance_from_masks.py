"""Distance between masks via solenoid."""
def solenoid_distance_from_masks(mask_a, mask_b, depth=20):
    ta = [int(v) & 1 for row in mask_a for v in row][:depth]
    tb = [int(v) & 1 for row in mask_b for v in row][:depth]
    for k in range(min(len(ta), len(tb))):
        if ta[k] != tb[k]:
            return 1.0 - 2.0 ** (-k)
    return 0.0
