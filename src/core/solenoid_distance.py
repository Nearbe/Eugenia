"""Solenoid distance: 2^(-k) where k is first differing bit."""


def solenoid_distance(traj_a: list[int], traj_b: list[int]) -> float:
    for k in range(min(len(traj_a), len(traj_b))):
        if traj_a[k] != traj_b[k]:
            return 2.0 ** (-k)
    return 0.0