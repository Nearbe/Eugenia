#  Copyright (c) 2026.
#  ╔═══════════════════════════════════╗
#  ║ Русский  ║ English    ║ Ελληνικά  ║
#  ║══════════║════════════║═══════════║
#  ║ Евгений  ║ Eugene     ║ Εὐγένιος  ║
#  ║ Евгения  ║ Eugenia    ║ Εὐγενία   ║
#  ║ Евгеника ║ Eugenics   ║ Εὐγενική  ║
#  ║ Евгениос ║ Eugenius   ║ Εὐγένιος  ║
#  ║ Женя     ║ Zhenya     ║ Ζένια     ║
#  ╚═══════════════════════════════════╝

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..states.fullness_share import FullnessShare


def _fullness_share(value: object) -> FullnessShare | None:
    """Return ``value`` as a fullness share when it belongs to that layer."""
    from ..states.fullness_share import FullnessShare

    return value if isinstance(value, FullnessShare) else None
