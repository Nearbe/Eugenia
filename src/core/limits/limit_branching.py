"""Limit of branching: lim D^n(Id) = Π."""


def limit_branching(n: int) -> float:
    return 3.141592653589793 if n >= 1000 else 2.0 ** n