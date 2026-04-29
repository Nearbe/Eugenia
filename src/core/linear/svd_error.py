"""SVD reconstruction error: ||W - W_rec||_F / ||W||_F."""
from .mat_norm import mat_norm
from .mat_sub import mat_sub


def svd_error(W, W_rec):
    diff = mat_sub(list(W), list(W_rec))
    norm_W = mat_norm(list(W))
    return mat_norm(diff) / norm_W if norm_W > 1e-10 else 0.0