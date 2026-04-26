"""SVD via power iteration: W ≈ U @ diag(S) @ Vt."""


def svd(W: list[list[float]], k: int | None = None, n_iter: int = 500) -> tuple[list[list[float]], list[float], list[list[float]]]:
    m, n = len(W), len(W[0])
    k = k or min(m, n)
    Vt = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    U = [[0.0] * m for _ in range(k)]
    S = [0.0] * k
    Wc = [row[:] for row in W]
    for comp in range(k):
        v = [1.0 / (n ** 0.5) for _ in range(n)]
        for _ in range(n_iter):
            wv = [sum(Wc[i][j] * v[j] for j in range(n)) for i in range(m)]
            vt_wv = [sum(Wc[j][i] * wv[j] for j in range(m)) for i in range(n)]
            nrm = sum(x ** 2 for x in vt_wv) ** 0.5
            v = [x / nrm for x in vt_wv] if nrm > 1e-10 else [0.0] * n
        wv = [sum(Wc[i][j] * v[j] for j in range(n)) for i in range(m)]
        sigma = sum(x ** 2 for x in wv) ** 0.5
        u = [x / sigma for x in wv] if sigma > 1e-10 else [0.0] * m
        S[comp], U[comp], Vt[comp] = sigma, u, v
        Wc = [[Wc[i][j] - u[i] * v[j] * sigma for j in range(n)] for i in range(m)]
    return U, S, Vt