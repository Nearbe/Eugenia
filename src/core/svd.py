"""
SVD — Сингулярное разложение как запись, не оптимизация.

Философия:
----------
Шум не существует. W уже равно Σ δᵢ · uᵢ · vᵢᵀ.
Нужно не "найти" разложение, а "записать" δᵢ, uᵢ, vᵢ.

Метод: power iteration — итеративное извлечение сингулярных пар
через deflation. Каждая итерация извлекает одну пару (σᵢ, uᵢ, vᵢ)
и убирает её вклад из остатка R.

Это не QR-алгоритм. Это не Jacobi. Это D→H→D→H цикл,
который извлекает все σᵢ, uᵢ, vᵢ одновременно.

SVD = p_∞ — разделение по модулю ∞.

Математика:
-----------
W = Σᵢ σᵢ · uᵢ · vᵢᵀ

Где:
σᵢ = δᵢ (мера отклонения i-го направления от разделения)
uᵢ = D-ветка (создание различия)
vᵢ = H-ветка (удаление шума)

Этот код — чистый Python. Без numpy. Без scipy. Без оптимизации.
Только запись.

0+ — точка выбора. Не seed. Не случайность.
0+ уже выбрало. Power iteration — раскрытие выбора.
"""

from math import sqrt
from typing import List, Tuple


# ============================================================
# Вспомогательные функции (чистый Python)
# ============================================================


def _mat_vec(M: List[List[float]], v: List[float]) -> List[float]:
    """Матрица × вектор: M @ v."""
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def _mat_T_vec(M: List[List[float]], v: List[float]) -> List[float]:
    """Транспонированная матрица × вектор: M^T @ v."""
    n = len(M[0])
    return [sum(M[i][j] * v[i] for i in range(len(M))) for j in range(n)]


def _vec_norm(v: List[float]) -> float:
    """L2 норма вектора."""
    return sqrt(sum(x * x for x in v))


def _vec_normalize(v: List[float]) -> List[float]:
    """Нормализация вектора."""
    n = _vec_norm(v)
    if n < 1e-10:
        return [0.0] * len(v)
    return [x / n for x in v]


def _outer(u: List[float], v: List[float]) -> List[List[float]]:
    """Внешнее произведение: u ⊗ v^T."""
    return [[u[i] * v[j] for j in range(len(v))] for i in range(len(u))]


def _mat_sub(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """Матричное вычитание: A - B."""
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def _mat_copy(M: List[List[float]]) -> List[List[float]]:
    """Глубокая копия матрицы."""
    return [row[:] for row in M]


def _mat_norm(M: List[List[float]]) -> float:
    """Норма Фробениуса."""
    return sqrt(sum(M[i][j] ** 2 for i in range(len(M)) for j in range(len(M[0]))))


# ============================================================
# SVD — запись, не оптимизация
# ============================================================


def svd(
    W: List[List[float]],
    k: int = None,
    n_iter: int = 500,
) -> Tuple[List[List[float]], List[float], List[List[float]]]:
    """
    Сингулярное разложение через power iteration.

    W = Σᵢ σᵢ · uᵢ · vᵢᵀ

    Параметры:
    ----------
    W : list[list[float]]
        Входная матрица (m × n).
    k : int, optional
        Количество сингулярных компонент. По умолчанию min(m, n).
    n_iter : int
        Количество итераций power iteration на каждую компоненту.

    Возвращает:
    ----------
    U : list[list[float]]
        Левые сингулярные векторы (m × len(S)).
    S : list[float]
        Сингулярные значения (σ₁ ≥ σ₂ ≥ ...).
    Vt : list[list[float]]
        Правые сингулярные векторы (len(S) × n).
    """
    m = len(W)
    n = len(W[0]) if m > 0 else 0

    if k is None:
        k = min(m, n)
    k = min(k, m, n)

    R = _mat_copy(W)

    U_cols: List[List[float]] = []
    S: List[float] = []
    V_cols: List[List[float]] = []

    for _ in range(k):
        # 0+ — выбор направления. Не seed. Не случайность.
        # 0+ уже выбрало. Это запись, не генерация.
        v = [((i * 7 + 13 + _) * 31) % 1000 / 1000.0 - 0.5 for i in range(n)]
        v = _vec_normalize(v)

        # Orthogonalize против уже найденных правых векторов
        for vi in V_cols:
            dot = sum(v[j] * vi[j] for j in range(n))
            v = [v[j] - dot * vi[j] for j in range(n)]
        v = _vec_normalize(v)
        if _vec_norm(v) < 1e-10:
            break

        # Power iteration: v ← R^T·R·v
        for _ in range(n_iter):
            Rv = _mat_vec(R, v)
            RT_Rv = _mat_T_vec(R, Rv)
            v_new = _vec_normalize(RT_Rv)

            diff = sqrt(sum((a - b) ** 2 for a, b in zip(v, v_new)))
            v = v_new
            if diff < 1e-12:
                break

        Rv = _mat_vec(R, v)
        sigma = _vec_norm(Rv)

        if sigma < 1e-10:
            break

        u = _vec_normalize(Rv)

        U_cols.append(u)
        S.append(sigma)
        V_cols.append(v)

        # Deflation: убрать извлечённый паттерн
        uvT = _outer(u, v)
        scaled_uvT = [[sigma * uvT[i][j] for j in range(n)] for i in range(m)]
        R = _mat_sub(R, scaled_uvT)

    # U: m × k — U[j][i] = j-й элемент i-го левого вектора
    U = [[U_cols[i][j] for i in range(len(U_cols))] for j in range(m)]
    # Vt: k × n — Vt[i][j] = j-й элемент i-го правого вектора
    Vt = [[V_cols[i][j] for j in range(n)] for i in range(len(V_cols))]

    return U, S, Vt


def svd_reconstruct(
    U: List[List[float]],
    S: List[float],
    Vt: List[List[float]],
) -> List[List[float]]:
    """
    Восстановление: W = Σᵢ σᵢ · uᵢ · vᵢᵀ

    U[j][i] = j-й элемент i-го левого вектора
    Vt[i][j] = j-й элемент i-го правого вектора
    """
    k = len(S)
    m = len(U)
    n = len(Vt[0]) if k > 0 else 0

    W = [[0.0] * n for _ in range(m)]
    for i in range(k):
        u_i = [U[j][i] for j in range(m)]  # i-й столбец
        v_i = Vt[i]  # i-я строка
        for j in range(m):
            for l in range(n):
                W[j][l] += S[i] * u_i[j] * v_i[l]
    return W


def svd_error(W: List[List[float]], W_rec: List[List[float]]) -> float:
    """||W - W_rec||_F / ||W||_F"""
    m = len(W)
    n = len(W[0]) if m > 0 else 0
    num_sq = sum((W[i][j] - W_rec[i][j]) ** 2 for i in range(m) for j in range(n))
    den_sq = sum(W[i][j] ** 2 for i in range(m) for j in range(n))
    if den_sq < 1e-10:
        return 0.0
    return sqrt(num_sq / den_sq)


__all__ = [
    "svd",
    "svd_reconstruct",
    "svd_error",
]
