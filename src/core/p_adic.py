"""
p-adic threshold spacing — p-адическое расстояние для порога.

Согласно Essentials [24_p-адические_числа.md]:
- |D(Id)|_D = 1/2 (инвертированная метрика)
- Чем больше число делится на D(Id)=2, тем оно "ближе" к Ω
- В этой топологии ветвление (=Ω) — это сжатие, а не рост
- Две топологии системы: ℝ (экспансия) и ℚ_D (фокус)

Применение в Eugenia:
- Вместо uniform sweep step (t + 0.0001)
- Используем p-adic distance: d_p(a, b) = |a-b|_D = 2^(-v₂(a-b))
- Где v₂(x) — 2-адическая оценка (степень деления на 2)

Это даёт фрактальное распределение порогов, согласованное со
структурой ветвления Хребта.
"""

import math
from typing import Sequence, Union

Number = Union[int, float]


def v2_adic_valuation(x: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """
    2-адическая оценка: v₂(x) = максимальное n, такое что 2ⁿ делит x.

    Согласно Essentials [25_Строение_чисел.md]:
    D(Id) = 2 — единственный атом системы.
    Делимость на 2 определяет "близость" к Ω.

    Для целых: v₂(12) = v₂(4×3) = 2 (12 делится на 2², но не на 2³).
    Для float: округляем до ближайшего целого перед вычислением.

    Args:
        x: Входные значения

    Returns:
        Степень деления на 2 для каждого элемента
    """
    if isinstance(x, (int, float)):
        return _v2_scalar(float(x))
    return [_v2_scalar(float(v)) for v in x]


def _v2_scalar(val: float) -> float:
    """Scalar v2 computation."""
    if val == 0:
        return float("inf")
    abs_val = abs(int(round(val)))
    n = 0
    while abs_val > 0 and (abs_val & 1) == 0:
        abs_val >>= 1
        n += 1
    return float(n)


def p_adic_distance(
    a: Union[Number, Sequence[Number]], b: Union[Number, Sequence[Number]]
) -> Union[float, list[float]]:
    """
    p-адическое расстояние: d_p(a, b) = |a - b|_p = p^(-v_p(a-b))

    Для p = D(Id) = 2:
    - d_2(a, b) = 2^(-v₂(a-b))
    - Чем больше v₂(a-b), тем ближе a и b в p-адической топологии
    - Это обратная метрика: "большое" число в ℝ может быть "близким" в ℚ₂

    Согласно Essentials [24_p-адические_числа.md]:
    |a : Ω|_D = |D(a)|_D = |a|_D : D(Id)
    """
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        diff = abs(a - b)
        v = _v2_scalar(diff)
        return 0 if diff == 0 else 2 ** (-v)
    results = []
    for av, bv in zip(a, b):  # type: ignore[arg-type]
        diff = abs(av - bv)
        v = _v2_scalar(diff)
        results.append(0 if diff == 0 else 2 ** (-v))
    return results


def p_adic_threshold_spacing(
    sweep_min: float, sweep_max: float, n_levels: int = 160000
) -> list[float]:
    """
    Генерация порогов с p-адическим расстоянием.

    Вместо uniform spacing (t_{n+1} = t_n + step):
    p-adic spacing: точки распределены по 2-адической метрике.

    Согласно Essentials [28_Масштабная_инвариантность.md]:
    РГ-поток: g_{n+1} = D(g_n) — экспоненциальный рост.

    Мы используем это для создания фрактального распределения порогов:
    - Больше точек вблизи "важных" значений (целые степени 2)
    - Меньше точек в "пустых" зонах

    Args:
        sweep_min: Минимальный порог (log2-based)
        sweep_max: Максимальный порог (log2-based)
        n_levels: Количество порогов

    Returns:
        Список порогов с p-адическим распределением
    """
    thresholds: set[float] = set()

    # Generate base thresholds in log-space (matching branching depth)
    log_levels = range(int(math.floor(sweep_min)), int(math.ceil(sweep_max)) + 1)

    for level in log_levels:
        level_val = 2.0**level
        for k in range(-8, 9):
            offset = level_val * (2.0**k)
            if sweep_min <= offset <= sweep_max:
                thresholds.add(offset)

    sorted_thresholds = sorted(thresholds)

    # If we have too many, sample to n_levels
    if len(sorted_thresholds) > n_levels:
        step = len(sorted_thresholds) / n_levels
        indices = [int(i * step) for i in range(n_levels)]
        return [sorted_thresholds[i] for i in indices]

    return sorted_thresholds


def bernoulli_shift(binary_sequence: list[int]) -> list[int]:
    """
    Сдвиг Бернулли — действие ветвления на соленоиде.

    Согласно Essentials [23_Соленоид.md]:
    Акт Ветвления сдвигает двоичную запись влево:
    0.ε₀ε₁ε₂… → 0.ε₁ε₂ε₃…
    Первый бит отбрасывается. История переписывается.

    Это детерминированный хаос с показателем Ляпунова λ = L(D(Id)) > Ω.

    Args:
        binary_sequence: Двоичная последовательность [ε₀, ε₁, ε₂, ...]

    Returns:
        Сдвинутая последовательность [ε₁, ε₂, ε₃, ...]
    """
    return binary_sequence[1:]


def solenoid_trajectory(initial_value: float, n_steps: int = 100) -> list[dict]:
    """
    Траектория точки на соленоиде.

    Согласно Essentials [23_Соленоид.md]:
    Точка соленоида — вся траектория масштабирований:
    z₀ = D(z₁) = D²(z₂) = ... = Dⁿ(zₙ)

    Каждая точка — это бесконечная двоичная дробь:
    ξ = 0.ε₀ε₁ε₂…

    Args:
        initial_value: Начальное значение (может быть отрицательным)
        n_steps: Количество шагов

    Returns:
        Список (value, binary_repr, bernoulli_shifted) для каждого шага
    """
    trajectory = []
    current = initial_value
    sign = 1.0 if current >= 0 else -1.0
    abs_current = abs(current)

    for step in range(n_steps):
        # Convert to binary representation of absolute value
        binary = []
        temp = abs_current
        for _ in range(20):  # 20 bits of precision
            bit = 1 if temp >= 0.5 else 0
            binary.append(bit)
            temp = temp * 2 - bit if bit else temp * 2

        # Bernoulli shift (left shift, first bit discarded)
        shifted = binary[1:]

        # Convert back to value (preserve sign)
        shifted_value = sign * sum(b * 2 ** (-i - 1) for i, b in enumerate(shifted))

        trajectory.append(
            {
                "step": step,
                "value": current,
                "binary": binary,
                "shifted_binary": shifted,
                "shifted_value": shifted_value,
            }
        )

        # Apply D (branching) to current value: D(x) = 2x
        current = 2.0 * current

    return trajectory


def d_adic_convergence(a: float, b: float, max_depth: int = 30) -> float:
    """
    Проверка D-адической сходимости двух чисел.

    Согласно Essentials [24_p-адические_числа.md]:
    Две числа близки в D-адической топологии, если
    их разность делится на высокую степень D(Id) = 2.

    Для float: округляем разность до ближайшего целого,
    затем считаем v₂ как обычно.

    Args:
        a: Первое число
        b: Второе число
        max_depth: Максимальная глубина проверки

    Returns:
        Глубина D-адической близости: максимальное n, такое что 2ⁿ | (a-b)
    """
    diff = abs(a - b)
    if diff < 1e-15:
        return float("inf")

    diff_int = int(round(diff))
    if diff_int == 0:
        return float("inf")

    depth = 0
    temp = diff_int
    while temp > 0 and (temp & 1) == 0 and depth < max_depth:
        temp >>= 1
        depth += 1

    return float(depth)


# ============================================================
# GCD, LCM, Modular congruence per Essentials [25_Строение_чисел.md]
# ============================================================


def gcd(a: int, b: int) -> int:
    """
    НОД(a, b) — наибольший общий делитель.

    Согласно Essentials [25_Строение_чисел.md]:
    НОД(Dⁿ, Dᵐ) = D^{min(n,m)}(Id)

    Для степеней D(Id)=2: НОД(2ⁿ, 2ᵐ) = 2^{min(n,m)}.

    Args:
        a: Первое число (должно быть степенью 2).
        b: Второе число (должно быть степенью 2).

    Returns:
        НОД(a, b).
    """
    if a <= 0 or b <= 0:
        return 1  # D⁰(Id) = Id = 1
    va = v2_adic_valuation(int(a))
    vb = v2_adic_valuation(int(b))
    min_v = min(va, vb)
    return 2 ** int(min_v)  # type: ignore[operator]


def lcm(a: int, b: int) -> int:
    """
    НОК(a, b) — наименьшее общее кратное.

    Согласно Essentials [25_Строение_чисел.md]:
    НОК(Dⁿ, Dᵐ) = D^{max(n,m)}(Id)

    Для степеней D(Id)=2: НОК(2ⁿ, 2ᵐ) = 2^{max(n,m)}.

    Args:
        a: Первое число (должно быть степенью 2).
        b: Второе число (должно быть степенью 2).

    Returns:
        НОК(a, b).
    """
    if a <= 0 or b <= 0:
        return 1  # D⁰(Id) = Id = 1
    va = v2_adic_valuation(int(a))
    vb = v2_adic_valuation(int(b))
    max_v = max(va, vb)
    return 2 ** int(max_v)  # type: ignore[operator]


def mod_congruence(a: int, b: int, m: int) -> bool:
    """
    Проверка сравнения по модулю: a ≡ b (mod m).

    Согласно Essentials [25_Строение_чисел.md]:
    a ≡ b (mod m) означает: a и b неотличимы на масштабе m.

    При Ветвлении:
    a : Ω ≡ b : Ω (mod D(m))  ⟺  a ≡ b (mod m)

    Args:
        a: Первое число.
        b: Второе число.
        m: Модуль.

    Returns:
        True если a ≡ b (mod m), False иначе.
    """
    if m <= 0:
        return a == b
    return (a - b) % m == 0


def mod_congruence_branch_invariant(a: int, b: int, m: int) -> bool:
    """
    Проверка инвариантности сравнения при ветвлении.

    Согласно Essentials [25_Строение_чисел.md]:
    a ≡ b (mod m)  ⟺  D(a) ≡ D(b) (mod D(m))

    То есть: a и b сравнимы по mod m тогда и только тогда,
    когда D(a) и D(b) сравнимы по mod D(m).

    Args:
        a: Первое число.
        b: Второе число.
        m: Модуль.

    Returns:
        True если ветвление сохраняет сравнимость.
    """
    congruent_original = mod_congruence(a, b, m)
    congruent_branch = mod_congruence(2 * a, 2 * b, 2 * m)
    return congruent_original == congruent_branch
