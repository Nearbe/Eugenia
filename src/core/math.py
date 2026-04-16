import numpy as np


def safe_divide(a, b):
    '''Безопасное деление: a/b if b!=0 else 0'''
    return np.divide(a, b, where=(b!=0), out=np.zeros_like(a))


def div_safe(a, b):
    return safe_divide(a, b)


def resolve_potential(x):
    '''max(x, 0)'''
    return np.maximum(x, 0.0)


def is_potential(x):
    return x != 0


def normalize_vector_safe(v):
    '''v / ||v|| if ||v|| > 1e-8 else v'''
    norm = np.linalg.norm(v)
    return v / norm if norm > 1e-8 else v


def has_potential(x):
    return np.any(x != 0)
