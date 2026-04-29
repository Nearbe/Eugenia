"""Deep copy of matrix."""


def mat_copy(M: list[list[float]]) -> list[list[float]]:
    return [row[:] for row in M]