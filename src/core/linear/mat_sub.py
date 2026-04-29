"""Matrix subtraction: A - B."""


def mat_sub(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]