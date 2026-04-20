"""
Delta field operators — Операторы дельта-поля.

Дельта-поле: D = log2(X+1) - log2(2^Q - X)
Отображает X ∈ [0, 2^Q - 1] в D ∈ [-Q, +Q].

Q = 10 (D_f = фрактальная размерность) — цикл из 10 шагов (0-9),
каждый шаг = смена масштаба. Значение 1.0 разлагается на 9 цифр слева
(минусовый диапазон) и 9 цифр справа (плюсовой диапазон).

1024 = 2¹⁰ = D¹⁰(Id) — 10 уровней ветвления.
L(1024) = log2(1024) = 10 — глубина рекурсии Хребта.
"""

import math
from typing import Sequence, Union

Number = Union[int, float]

# Fractal dimension (Q) — цикл масштабов: 10 шагов (0-9)
Q = 10
_RANGE = 2**Q  # 1024


def delta_field(x_val: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """
    Дельта-поле: D = log2(X+1) - log2(2^Q - X).

    Отображает X ∈ [0, 2^Q - 1] в D ∈ [-Q, +Q].

    D = +Q при X=2^Q-1 → ветвление (a:Ω), Q уровней глубины
    D = −Q при X=0 → сжатие (a:D(Id)^Q)
    D = 0 при X=(2^Q-1)/2 → баланс

    2^Q = 2^10 = 1024 = D^10(Id) — 10 уровней ветвления (Хребет).
    L(1024) = log2(1024) = 10.
    """
    if isinstance(x_val, (int, float)):
        x = max(min(float(x_val), _RANGE - 1.001), 0.0)
        return math.log2(x + 1.0) - math.log2(_RANGE - x)
    return [
        math.log2(max(min(float(x), _RANGE - 1.001), 0.0) + 1.0)
        - math.log2(_RANGE - max(min(float(x), _RANGE - 1.001), 0.0))
        for x in x_val
    ]


def inverse_delta_field(d_val: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """
    Обратное отображение: D → X.

    D = log2(X+1) - log2(2^Q - X)
    X = (2^Q * 2^D - 1) / (2^D + 1)
    """
    if isinstance(d_val, (int, float)):
        exp_d = 2.0**d_val  # 2^d_val, not e^d_val — inverse of log2
        return (_RANGE * exp_d - 1.0) / (exp_d + 1.0)
    return [(_RANGE * (2.0**d) - 1.0) / ((2.0**d) + 1.0) for d in d_val]
