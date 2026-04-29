"""Frobenius norm: ||M||_F = sqrt(sum(M_ij^2))."""


def mat_norm(M: list[list[float]]) -> float:
    return sum(M[i][j] ** 2 for i in range(len(M)) for j in range(len(M[0]))) ** 0.5