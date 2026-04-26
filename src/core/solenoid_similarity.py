"""Solenoid similarity: 2^(-k) for first differing bit."""


def solenoid_similarity(traj_a: list[int], traj_b: list[int]) -> float:
    for k in range(min(len(traj_a), len(traj_b))):
        if traj_a[k] != traj_b[k]:
            return 2.0 ** (-k)
    return 1.0