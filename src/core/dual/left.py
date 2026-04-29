"""Left chain power."""
from .constants import D_ID


def left(pyr_level):
    return D_ID ** (pyr_level - 1)