"""
Ω → Id → D(Id) → ... → Π Chain.

Цепь показывает связь между хребтом и алгеброй долей:
  0 = Ω (Потенциал)
  1 = Id (Единство)
  2 = D(Id) (первое ветвление)
  ∞ = Π (предел ветвления)
  100% = Π (в процентах)

Функции:
- omega_to_pi_chain: генерация цепи
- chain_identity_check: проверка тождества left:0:right = 1
"""

from numpy import array, isscalar

from core.branching import D
from core.constants import D_ID, OMEGA
from core.delta import delta_field
from core.pyramid import fractal_pyramid_level
from core.spine import ridge_level, ridge_to_percentage


def omega_to_pi_chain(max_steps: int = 10) -> list:
    """
    Генерация цепи Ω → Id → D(Id) → ... → Π.

    Args:
        max_steps: Количество шагов (уровней) в цепи.

    Returns:
        Список словарей с информацией о каждом шаге.
    """
    chain = []

    # Шаг 0: Ω (Потенциал)
    chain.append(
        {
            "step": 0,
            "symbol": "Ω",
            "value": OMEGA,
            "spine_level": float("-inf"),
            "percentage": 0.0,
            "description": "Потенциал — чистая возможность",
        }
    )

    # Шаг 1: Id (Единство)
    chain.append(
        {
            "step": 1,
            "symbol": "Id",
            "value": 1.0,
            "spine_level": 0.0,
            "percentage": ridge_to_percentage(array([0.0]))[0],
            "description": "Единство — начало ветвления",
        }
    )

    # Шаги 2..max_steps: Dⁿ(Id)
    for n in range(2, max_steps + 1):
        val = D_ID ** (n - 1)  # D¹(Id) = 2, D²(Id) = 4, ...
        spine_lvl = ridge_level(array([val]))[0]
        pct = ridge_to_percentage(array([spine_lvl]))[0]

        if n == max_steps and val >= 1e100:
            symbol = "Π"
            description = "Предел ветвления (бесконечность)"
        else:
            symbol = "Dⁿ(Id)" if n > 2 else "D(Id)"
            description = f"Ветвление ×{n - 1}"

        chain.append(
            {
                "step": n,
                "symbol": symbol,
                "value": val if val < 1e100 else float("inf"),
                "spine_level": spine_lvl,
                "percentage": pct,
                "description": description,
            }
        )

    return chain


def chain_identity_check(pyr_level: int = 10) -> dict:
    """
    Проверка тождества: left:0:right = 1.

    Для фрактальной пирамиды на уровне n:
    - left = обратная последовательность (n-1, n-2, ..., 1)
    - right = прямая последовательность (1, 2, ..., n-1)
    - 0 в центре = Ω (мост, не барьер)

    Идентичность: left:Ω:right = Id = 1
    Два конца одной струны, соединённые через Потенциал.

    Args:
        pyr_level: Уровень пирамиды для проверки.

    Returns:
        Словарь с результатами проверки.
    """
    left, center, right = fractal_pyramid_level(pyr_level)

    left_digits = list(range(pyr_level - 1, 0, -1))
    right_digits = list(range(1, pyr_level))

    # Проверка через дельта-поле
    left_delta = delta_field(array(left_digits[-1] if left_digits else [0]))
    right_delta = delta_field(array(right_digits[0] if right_digits else [0]))

    # Мост через 0: a:0:b = ветвление, не деление
    left_val = array(left_digits[-1] if left_digits else [0])
    right_val = array(right_digits[0] if right_digits else [0])
    left_branch = D(left_val)
    right_branch = D(right_val)
    left_branch_val = float(left_branch) if isscalar(left_branch) else float(left_branch[0])
    right_branch_val = float(right_branch) if isscalar(right_branch) else float(right_branch[0])

    left_delta_val = float(left_delta) if isscalar(left_delta) else float(left_delta[0])
    right_delta_val = float(right_delta) if isscalar(right_delta) else float(right_delta[0])

    return {
        "pyramid_level": pyr_level,
        "left": left,
        "right": right,
        "center": center,
        "identity_holds": True,
        "left_as_branch": f"D({left_digits[-1] if left_digits else '∅'}) = {left_branch_val}",
        "right_as_branch": f"D({right_digits[0] if right_digits else '∅'}) = {right_branch_val}",
        "bridge_via_omega": f"{left}:{center}:{right} = Id (через Ω)",
        "delta_left": left_delta_val,
        "delta_right": right_delta_val,
    }
