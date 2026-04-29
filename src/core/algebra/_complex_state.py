from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..states.complex_plane import ComplexState


def _complex_state(value: object) -> ComplexState | None:
    """Return ``value`` as a complex state when it belongs to that layer."""
    from ..states.complex_plane import ComplexState

    return value if isinstance(value, ComplexState) else None
