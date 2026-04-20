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

Это даёт фрактальное распрежение порогов, согласованное со
структурой ветвления Хребта.
"""

from numpy import (
    abs,
    arange,
    asarray,
    float64,
    linspace,
    log2,
    ndarray,
    searchsorted,
    unique,
    where,
    zeros_like,
)


def v2_adic_valuation(x: ndarray) -> ndarray:
    """
    2-адическая оценка: v₂(x) = максимальное n, такое что 2ⁿ делит x.

    Согласно Essentials [25_Строение_чисел.md]:
    D(Id) = 2 — единственный атом системы.
    Делимость на 2 определяет "близость" к Ω.

    Args:
        x: Входные значения

    Returns:
        Степень деления на 2 для каждого элемента
    """
    x = asarray(x, dtype=float64)
    result = zeros_like(x)

    # For each non-zero value, count factors of 2
    mask = x != 0
    result[mask] = [int(log2(abs(int(round(x_val))))) if x_val != 0 else 0 for x_val in x[mask]]

    # Handle zeros: v₂(0) = ∞ (zero is divisible by any power of 2)
    result[~mask] = float("inf")

    return result


def p_adic_distance(a: ndarray, b: ndarray) -> ndarray:
    """
    p-адическое расстояние: d_p(a, b) = |a - b|_p = p^(-v_p(a-b))

    Для p = D(Id) = 2:
    - d_2(a, b) = 2^(-v₂(a-b))
    - Чем больше v₂(a-b), тем ближе a и b в p-адической топологии
    - Это обратная метрика: "большое" число в ℝ может быть "близким" в ℚ₂

    Согласно Essentials [24_p-адические_числа.md]:
    |a : Ω|_D = |D(a)|_D = |a|_D : D(Id)
    """
    diff = abs(asarray(a, dtype=float64) - asarray(b, dtype=float64))
    v = v2_adic_valuation(diff)

    # |x|_D = 2^(-v₂(x))
    return where(diff == 0, 0, 2 ** (-v))


def p_adic_threshold_spacing(sweep_min: float, sweep_max: float, n_levels: int = 160000) -> ndarray:
    """
    Генерация порогов с p-адическим расстоянием.

    Вместо uniform spacing (t_{n+1} = t_n + step):
    p-adic spacing: точки распределены по 2-адической метрике.

    Согласно Essentials [28_Масштабная_инвариантность.md]:
    РГ-поток: g_{n+1} = D(g_n) — экспоненциальный рост.

    Мы используем это для создания фрактального распрежения порогов:
    - Больше точек вблизи "важных" значений (целые степени 2)
    - Меньше точек в "пустых" зонах

    Args:
        sweep_min: Минимальный порог (log2-based)
        sweep_max: Максимальный порог (log2-based)
        n_levels: Количество порогов

    Returns:
        Массив порогов с p-адическим распределением
    """
    # Generate base thresholds in log-space (matching branching depth)
    # Each level n corresponds to Dⁿ(I'd) = 2ⁿ
    log_levels = arange(sweep_min, sweep_max, 0.5)  # Coarse log-scale grid

    # For each level, generate p-adic refined thresholds
    thresholds = []
    for level in log_levels:
        # At each branching level, add refined thresholds
        # using p-adic distance from the branching point
        level_val = 2**level  # Dⁿ(Id)
        refined = []

        for k in range(-8, 9):  # v₂ range
            # p-adic offset from branching point
            offset = level_val * (2**k)
            if sweep_min <= offset <= sweep_max:
                refined.append(offset)

        thresholds.extend(refined)

    thresholds = unique(array(thresholds))

    # If we have too many, sample to n_levels
    if len(thresholds) > n_levels:
        indices = searchsorted(thresholds, linspace(thresholds[0], thresholds[-1], n_levels))
        thresholds = thresholds[indices]

    return thresholds


def bernoulli_shift(binary_sequence: ndarray) -> ndarray:
    """
    Сдвиг Бернулли — действие ветвления на соленоиде.

    Согласно Essentials [23_Соленоид.md]:
    Акт Ветвления сдвигает двоичную запись влеов:
    0.ε₀ε₁ε₂… → 0.ε₁ε₂ε₃…
    Первый бит отбрасывается. История переписывается.

    Это детерминированный хаос с показателем Ляпунова λ = L(D(Id)) > Ω.

    Args:
        binary_sequence: Двоичная последовательность [ε₀, ε₁, ε₂, ...]

    Returns:
        Сдвинутая последовательность [ε₁, ε₂, ε₃, ...]
    """
    return binary_sequence[1:]


def solenoid_trajectory(initial_value: float, n_steps: int = 100) -> list:
    """
    Траектория точки на соленоиде.

    Согласно Essentials [23_Соленоид.md]:
    Точка соленоида — вся траектория масштабирований:
    z₀ = D(z₁) = D²(z₂) = ... = Dⁿ(zₙ)

    Каждая точка — это бесконечная двоичная дробь:
    ξ = 0.ε₀ε₁ε₂…

    Args:
        initial_value: Начальное значение
        n_steps: Количество шагов

    Returns:
        Список (value, binary_repr, bernoulli_shifted) для каждого шага
    """
    trajectory = []
    current = initial_value

    for _ in range(n_steps):
        # Convert to binary representation
        binary = []
        temp = abs(current)
        for _ in range(20):  # 20 bits of precision
            bit = 1 if temp >= 0.5 else 0
            binary.append(bit)
            temp = temp * 2 - bit if bit else temp * 2

        # Bernoulli shift
        shifted = binary[1:]

        # Convert back to value
        shifted_value = sum(b * 2 ** (-i - 1) for i, b in enumerate(shifted))

        trajectory.append(
            {
                "step": _,
                "value": current,
                "binary": binary,
                "shifted_binary": shifted,
                "shifted_value": shifted_value,
            }
        )

        # Apply D (branching) to current value
        current = 2.0 * current

    return trajectory


def d_adic_convergence(a: float, b: float, max_depth: int = 30) -> float:
    """
    Проверка D-адической сходимости двух чисел.

    Согласно Essentials [24_p-адические_числа.md]:
    Две числа близки в D-адической топологии, если
    их разность делится на высокую степень D(Id) = 2.

    Args:
        a: Первое число
        b: Второе число
        max_depth: Максимальная глубина проверки

    Returns:
        Глубина D-адической близости: максимальное n, такое что 2ⁿ | (a-b)
    """
    diff = abs(a - b)
    if diff == 0:
        return float("inf")  # Identical in all D-adic metrics

    depth = 0
    temp = diff
    while temp > 1e-15 and temp % 2 == 0:
        temp /= 2
        depth += 1

    return min(depth, max_depth)
