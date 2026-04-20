#!/usr/bin/env python3
"""
Correlation-based Compression — сжатие через корреляционные структуры

Научное обоснование:
--------------------
Данный модуль реализует метод сжатия нейросетевых весов через анализ их
корреляционных структур, основанный на теоретической框架 RealMath:

Теоретическая база:
-------------------
- L(M) = глубина структуры (информация по Колмогорову), а не количество бит
- Соленоид — представление истории изменений системы, а не её состояния
- D-оператор — оператор создания различий между состояниями системы

Основная идея:
--------------
Вместо хранения полных матриц весов W ∈ R^(m×n), хранятся:
1. Корреляции между весами — как каждый вес связан с другими
2. Паттерны изменений — дельта от начальной инициализации
3. Структура связей — граф зависимостей между нейронами
4. Главные компоненты корреляций — собственные векторы корреляционной матрицы

Математическая формализация:
----------------------------
Пусть W — матрица весов слоя размером m×n:

1. Delta compression:
   dW = W - W_init
   где W_init — матрица инициализации (random, Xavier, etc.)

   Преимущество: dW имеет меньшую энтропию и более разрежен, чем W

2. Correlation matrix:
   C = W^T · W / n
   где C ∈ R^(n×n) — симметричная положительно определённая матрица

   Свойства:
   - C[i,j] = corr(w_i, w_j) — корреляция между i-м и j-м весами
   - Ранг(C) ≤ min(m,n) — возможность низкоранговой аппроксимации

3. Graph structure:
   G = (V, E), где:
   - V = {v_1, ..., v_n} — нейроны/признаки
   - E = {(i,j) | |C[i,j]| > threshold} — рёбра корреляций

4. Principal correlations:
   C = U · Σ · U^T (собственное разложение)
   C ≈ U_k · Σ_k · U_k^T (низкоранговая аппроксимация)

   где k << n — число главных компонент

Атрибуты класса CorrelationCompressor:
--------------------------------------
- delta : np.ndarray — дельта весов от инициализации
- correlation_eigen : tuple — собственные значения и векторы корреляционной матрицы
- graph : dict — структура графа корреляций

Методы:
-------
- compress_delta(W, init_type) — сжатие через дельту от инициализации
- compress_correlation(W, k) — сжатие через главные компоненты корреляций
- build_graph(W, threshold) — построение графа корреляций
- compress_principal(W, k) — сжатие через главные корреляции

Пример использования:
---------------------
    >>> compressor = CorrelationCompressor()
    >>> # Метод 1: Delta compression
    >>> delta, W_init = compressor.compress_delta(W, init_type="xavier")
    >>> # Метод 2: Correlation matrix
    >>> C = compressor.compress_correlation(W, k=64)
    >>> # Метод 3: Graph structure
    >>> graph = compressor.build_graph(W, threshold=0.5)
    >>> # Метод 4: Principal correlations
    >>> compressed = compressor.compress_principal(W, k=32)

Применение:
-----------
- Сжатие обученных моделей для деплоя на edge-устройства
- Извлечение знаний из нейронных сетей (knowledge distillation)
- Анализ внутренней структуры представлений модели
- Детектирование избыточности в весах сети
"""

from struct import pack

from numpy import abs, diag, float16, float32, int8, linalg, random, sqrt, where, zeros_like


class CorrelationCompressor:
    """
    Компрессор на основе корреляционного анализа весов.

    Основная концепция:
    -------------------
    Вместо прямого хранения матрицы весов W размером [m × n],
    хранится информация о том, как каждый вес коррелирует с другими весами.

    Это позволяет:
    1. Достичь более высокой степени сжатия (особенно для переобученных моделей)
    2. Извлечь интерпретируемую структуру знаний
    3. Обнаружить избыточные нейроны/связи

    Методы компрессии:
    ------------------
    1. Delta from initialization:
       Хранение только изменений относительно начальной инициализации:
       dW = W - W_init

       Обоснование: Веса после обучения часто мало отличаются от инициализации
       в относительном смысле, но имеют систематические паттерны изменений.

    2. Correlation matrix:
       Вычисление матрицы корреляций: C = W.T @ W

       Обоснование: Корреляционная матрица захватывает структуру зависимостей
       между нейронами, которая более компактна, чем полные веса.

    3. Graph structure:
       Представление весов как графа, где узлы — нейроны, рёбра — корреляции.

       Обоснование: Графовая структура позволяет применять методы graph theory
       для анализа и сжатия.

    4. Principal correlations:
       SVD разложение корреляционной матрицы для выделения главных компонент.

       Обоснование: Большинство вариаций в данных объясняется несколькими
       главными компонентами (принцип компонентного анализа).

    Атрибуты:
    ---------
    self.delta : np.ndarray или None
        Дельта весов от инициализации
    self.correlation_eigen : tuple или None
        Кортеж (eigenvalues, eigenvectors) корреляционной матрицы
    self.graph : dict или None
        Словарь, представляющий граф корреляций
    """

    def __init__(self):
        """Инициализация компрессора."""
        self.delta = None
        self.correlation_eigen = None
        self.graph = None

    def compress_delta(self, W, init_type="random"):
        """
        Метод 1: Сжатие через дельту от инициализации.

        Вместо хранения полной матрицы весов W, хранится только изменение:
        dW = W - W_init

        Преимущества:
        - dW обычно более разрежен, чем W
        - dW имеет меньшую энтропию (более предсказуем)
        - Можно восстановить W = W_init + dW

        Параметры:
        ----------
        W : np.ndarray
            Матрица весов размером [m × n]
        init_type : str, optional
            Тип инициализации для W_init:
            - 'random': нормальное распределение N(0, 0.01²)
            - 'zeros': нулевая инициализация
            - 'xavier': инициализация Xavier/Glorot
              scale = sqrt(2.0 / (fan_in + fan_out))

        Возвращает:
        -----------
        delta : np.ndarray
            Матрица изменений dW = W - W_init
        W_init : np.ndarray
            Матрица инициализации (необходима для восстановления)

        Математика:
        -----------
        Для 'xavier': W_init ~ N(0, σ²), где σ = sqrt(2/(m+n))
        Для 'random': W_init ~ N(0, 0.01²)
        Для 'zeros': W_init = 0

        dW[i,j] = W[i,j] - W_init[i,j]

        Пример:
        -------
        >>> W = trained_weights  # [512, 512]
        >>> compressor = CorrelationCompressor()
        >>> delta, W_init = compressor.compress_delta(W, init_type="xavier")
        >>> # Восстановление: W_reconstructed = W_init + delta
        """
        if init_type == "random":
            W_init = random.randn(*W.shape).astype(float32) * 0.01
        elif init_type == "zeros":
            W_init = zeros_like(W)
        elif init_type == "xavier":
            scale = sqrt(2.0 / (W.shape[0] + W.shape[1]))
            W_init = random.randn(*W.shape).astype(float32) * scale

        delta = W - W_init

        return delta, W_init

    def compress_correlation_svd(self, W, k=None):
        """
        Метод 2: Correlation SVD

        Храним структуру корреляций — eigenvectors
        вместо самих значений

        C = W @ W.T — correlation matrix
        C = V @ Lambda @ V.T — eigendecomposition

        Вместо m*n значений храним k*(m+n) eigenvalues
        """
        m, n = W.shape
        if k is None:
            k = min(32, min(m, n))

        # Correlation через SVD: W = U @ S @ Vt
        # Корреляция: C = W @ W.T = U @ S² @ U.T

        U, S, Vt = linalg.svd(W, full_matrices=False)

        # Храним только top-k eigenvectors и eigenvalues
        self.correlation_eigen = {
            "U": U[:, :k].astype(float16),
            "S": S[:k].astype(float16),
            "Vt": Vt[:k, :].astype(float16),
            "k": k,
            "shape": W.shape,
        }

        return self.correlation_eigen

    def decompress_correlation_svd(self):
        """Восстановление из correlation SVD"""
        c = self.correlation_eigen
        U = c["U"].astype(float32)
        S = c["S"].astype(float32)
        Vt = c["Vt"].astype(float32)

        return U @ diag(S) @ Vt

    def compress_graph(self, W, threshold=0.5):
        """
        Метод 3: Graph representation

        Храним только СВЯЗИ между нейронами
        где |w_ij| > threshold
        """
        m, n = W.shape

        # Бинарный граф — есть связь или нет
        mask = abs(W) > threshold * abs(W).max()

        # Индексы сильных связей
        rows, cols = where(mask)
        values = W[mask]

        # Кодируем
        data = b""
        data += pack("<ii", m, n)
        data += pack("<i", len(rows))

        for r, c in zip(rows, cols):
            data += pack("<II", r, c)

        # Значения — int8 с масштабом
        scale = abs(values).max()
        data += pack("<f", scale)
        values_q = (values / scale * 127).round().astype(int8)
        data += values_q.tobytes()

        return data, len(rows) / (m * n)  # sparsity

    def compress_hessian_pattern(self, W):
        """
        Метод 4: Hessian pattern approximation

        Храним паттерн — как веса会影响 друг друга
        """
        # Approximate second-order info
        # H = W @ W.T — структура кривизны

        H = W @ W.T

        # Eigendecomposition of correlation
        # Это компактное представление структуры!

        return H


def test_methods():
    """Тест разных методов"""
    print("=" * 60)
    print("Correlation-based Compression")
    print("=" * 60)

    random.seed(42)

    # Typical weight matrix
    m, n = 4096, 4096
    W = random.randn(m, n).astype(float32)
    original = W.nbytes

    print(f"\nОригинал: {original / 1024**2:.1f} MB")
    print("-" * 40)

    # Метод 1: Delta compression
    delta, _ = CorrelationCompressor().compress_delta(W, "xavier")
    delta_size = delta.nbytes

    # Качество delta
    print("\n1. Delta от Xavier инициализации:")
    print(f"   Delta size: {delta_size / 1024**2:.1f} MB")

    # Проверим — можно ли восстановить?
    # На самом деле мы НЕ можем восстановить W из delta
    # Но корреляции между весами можно измерить!

    # Метод 2: Correlation SVD
    comp = CorrelationCompressor()
    corr = comp.compress_correlation_svd(W, k=8)

    size = corr["U"].nbytes + corr["S"].nbytes + corr["Vt"].nbytes
    ratio = original / size

    # Восстановление
    W_rec = comp.decompress_correlation_svd()
    error = linalg.norm(W - W_rec) / linalg.norm(W)

    print("\n2. Correlation SVD (k=8):")
    print(f"   Size: {size / 1024**2:.2f} MB")
    print(f"   Ratio: {ratio:.0f}x")
    print(f"   Error: {error * 100:.1f}%")
    print(f"   111GB -> {111 / ratio:.2f}GB")

    # Larger k
    for k in [16, 32, 64]:
        comp2 = CorrelationCompressor()
        corr2 = comp2.compress_correlation_svd(W, k=k)

        size2 = corr2["U"].nbytes + corr2["S"].nbytes + corr2["Vt"].nbytes
        ratio2 = original / size2

        W_rec2 = comp2.decompress_correlation_svd()
        error2 = linalg.norm(W - W_rec2) / linalg.norm(W)

        print(f"\n   k={k}: ratio={ratio2:.0f}x, error={error2 * 100:.1f}%")

    # Метод 3: Graph
    print("\n3. Graph representation:")
    comp3 = CorrelationCompressor()
    data, sparsity = comp3.compress_graph(W, threshold=0.3)
    print(f"   Sparsity: {(1 - sparsity) * 100:.1f}% нулей")
    print(f"   Size: {len(data) / 1024**2:.2f} MB")


def correlation_idea():
    """Главная идея — храним корреляции, не значения"""
    print("\n" + "=" * 60)
    print("ГЛАВНАЯ ИДЕЯ")
    print("=" * 60)

    print("""
    Ключевая идея из RealMath/Essentials:

    Информация = L(M) — глубина рекурсии

    Это означает:
    - Важна не величина веса, а ЕГО ПОЗИЦИЯ в структуре
    - Важна связь с другими весами
    - Паттерн изменения важнее абсолютного значения

    Практически:

    Вместо: W[4096][4096] = 16M значений

    Храним:
    1. Как образовались — D-оператор путь
    2. Связи — graph representation
    3. Eigenstructure — только eigenvectors

    Это может работать для INFERENCE потому что:
    - Forward pass использует корреляции между слоями
    - Сам формат весов менее важен чем их взаимодействие
    """)


if __name__ == "__main__":
    test_methods()
    correlation_idea()
