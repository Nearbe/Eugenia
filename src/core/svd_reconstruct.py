"""Reconstruct matrix from SVD."""
def svd_reconstruct(U, S, Vt):
    m, n = len(U[0]), len(Vt[0])
    return [[sum(S[k] * U[k][r] * Vt[k][c] for k in range(len(S))) for c in range(n)] for r in range(m)]
