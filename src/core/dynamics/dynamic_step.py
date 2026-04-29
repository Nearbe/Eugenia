from __future__ import annotations

from enum import StrEnum


class DynamicStep(StrEnum):
    """Elementary U-dynamic operators."""

    BRANCH = "D"
    COMPRESS = "H"
