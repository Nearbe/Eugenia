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
import math

import pytest

from core.foundations.constants import DELTA_MAX, DELTA_MIN, PIXEL_MAX, PIXEL_MIN
from core.operators.delta_field import delta_field
from core.operators.inverse_delta_field import inverse_delta_field


def test_delta_field_boundaries_are_finite_and_pinned():
    assert delta_field(PIXEL_MIN) == pytest.approx(DELTA_MIN)
    assert delta_field(PIXEL_MAX) == pytest.approx(DELTA_MAX)
    assert math.isfinite(delta_field(PIXEL_MIN))
    assert math.isfinite(delta_field(PIXEL_MAX))


def test_delta_field_clamps_out_of_range_values():
    assert delta_field(-10) == pytest.approx(delta_field(PIXEL_MIN))
    assert delta_field(300) == pytest.approx(delta_field(PIXEL_MAX))


def test_delta_field_inverse_roundtrip_representative_values():
    for value in [0.0, 1.0, 16.0, 127.5, 200.0, 254.0, 255.0]:
        assert inverse_delta_field(delta_field(value)) == pytest.approx(value, abs=1e-9)


def test_inverse_delta_field_clamps_delta_boundaries():
    assert inverse_delta_field(DELTA_MIN - 100.0) == pytest.approx(PIXEL_MIN)
    assert inverse_delta_field(DELTA_MAX + 100.0) == pytest.approx(PIXEL_MAX)


def test_delta_field_vector_contract():
    assert delta_field([0, 255]) == pytest.approx([DELTA_MIN, DELTA_MAX])
    assert inverse_delta_field([DELTA_MIN, DELTA_MAX]) == pytest.approx([PIXEL_MIN, PIXEL_MAX])
