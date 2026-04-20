"""
Delta field operators — Операторы дельта-поля.

Дельта-поле: D = log2(X+1) - log2(256-X)
Отображает X ∈ [0, 255] в D ∈ [-8, 8].

256 = 2⁸ = D⁸(Id) — 8 уровней ветвления.
L(256) = log2(256) = 8 — глубина рекурсии Хребта.
"""

import math
from typing import Sequence, Union

Number = Union[int, float]


def delta_field(x_val: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """
    Дельта-поле: D = log2(X+1) - log2(256-X).

    Отображает X ∈ [0, 255] в D ∈ [-8, 8].

    D = +8 при X=255 → ветвление (a:Ω), 8 уровней глубины
    D = −8 при X=0 → сжатие (a:D(Id)⁸)
    D = 0 при X=127.5 → mid-gray, баланс

    256 = 2⁸ = D⁸(Id) — 8 уровней ветвления (Хребет).
    L(256) = log2(256) = 8 — информация по Essentials [30_Информация.md].
    """
    if isinstance(x_val, (int, float)):
        x = max(min(float(x_val), 254.999), 0.0)
        return math.log2(x + 1.0) - math.log2(256.0 - x)
    return [
        math.log2(max(min(float(x), 254.999), 0.0) + 1.0)
        - math.log2(256.0 - max(min(float(x), 254.999), 0.0))
        for x in x_val
    ]


def inverse_delta_field(d_val: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """
    Обратное отображение: D → X.

    D = log2(X+1) - log2(256-X)
    X = (256*2^D - 1) / (2^D + 1)
    """
    if isinstance(d_val, (int, float)):
        exp_d = 2.0**d_val  # 2^d_val, not e^d_val — inverse of log2
        return (256.0 * exp_d - 1.0) / (exp_d + 1.0)
    return [(256.0 * (2.0**d) - 1.0) / ((2.0**d) + 1.0) for d in d_val]
