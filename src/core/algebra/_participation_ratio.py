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
    from ..states.rational import ParticipationRatio


def _participation_ratio(value: object) -> ParticipationRatio | None:
    """Return ``value`` as a participation ratio when it belongs to that layer."""
    from ..states.rational import ParticipationRatio

    return value if isinstance(value, ParticipationRatio) else None
