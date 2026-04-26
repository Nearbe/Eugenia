"""Dual function: f(x+vε) = f(x) + f'(x)·v·ε."""

def dual_func(x, v, f, df):
    return f(float(x)), df(float(x)) * float(v)
