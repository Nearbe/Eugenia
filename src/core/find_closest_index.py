"""Binary search: closest index to target."""


def find_closest_index(arr: list[float], target: float) -> int:
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        lo = mid + 1 if arr[mid] < target else hi
    return lo