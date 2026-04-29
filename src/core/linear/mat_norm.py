"""Frobenius norm: ||M||_F = sqrt(sum(M_ij^2))."""


def mat_norm(M) -> float:
    """Compute Frobenius norm of any matrix-like object."""
    total = 0.0
    for row in M:
        for val in row:
            total += float(val) ** 2
    return total**0.5
