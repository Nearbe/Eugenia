"""
Генератор паттерна «песочные часы» для уровня n.
"""


def generate_pattern(n: int) -> list[str]:
    """Генерирует строки паттерна «песочные часы» для уровня n."""
    if n == 1:
        # Маленький ромб 3x3
        center = "0:1:0:1:0"
        width = len(center)
    else:
        # Центральная строка: целые числа — определяет ширину фигуры
        left_center = ":".join(str(i) for i in range(n, 0, -1))
        right_center = ":".join(str(i) for i in range(1, n + 1))
        center = f"0:{left_center}:0:{right_center}:0"
        width = len(center)

    # Рамка: 1=1=1=...=1:0:1=1=...=1 (равенство вместо деления)
    # Ширина рамки = ширина центральной строки
    # left + 3(:0:) + right = width, и left = right для симметрии
    # ''.join(['1'] * n) даёт n цифр + (n-1) знаков '=' = 2n - 1
    # => 2 * (2n - 1) + 3 = width => n = (width - 1) // 4
    frame_n = (width - 1) // 4
    left_frame = "=".join(["1"] * frame_n)
    right_frame = "=".join(["1"] * frame_n)
    frame = f"{left_frame}:0:{right_frame}"

    lines: list[str] = [frame]

    # Верхние слои (k = 2 .. n)
    for k in range(2, n + 1):
        k_str = str(k)
        if k == 2:
            # Строка 2: 2:9.8.7.6.5.4.3.2.1:0:1.2.3.4.5.6.7.8.9:2
            left_dec = ".".join(str(i) for i in range(n, 0, -1))
            right_dec = ".".join(str(i) for i in range(1, n + 1))
            line = f"{k_str}:{left_dec}:0:{right_dec}:{k_str}"
        else:
            step = k - 1
            # Слева: step → 1
            left_digits = ":".join(str(i) for i in range(step, 0, -1))
            # Справа: 1 → step
            right_digits = ":".join(str(i) for i in range(1, step + 1))
            content = f"{left_digits}:0:{right_digits}"
            pad = (width - 2 * len(k_str) - len(content)) // 2
            line = f"{k_str}{' ' * pad}{content}{' ' * pad}{k_str}"
        lines.append(line)

    # Центральная строка
    lines.append(center)

    # Нижние слои (зеркальное отражение)
    for k in range(n, 1, -1):
        lines.append(lines[k - 1])

    # Нижняя рамка
    lines.append(frame)

    return lines


def print_pattern(n: int, labels: bool = True) -> None:
    """Выводит паттерн для уровня n с опциональными подписями."""
    lines = generate_pattern(n)
    width = len(lines[0])

    if labels:
        col_header1 = ""
        col_header2 = ""
        for pos in range(1, width + 1):
            if pos % 10 == 0:
                col_header1 += str(pos // 10)
            else:
                col_header1 += " "
            col_header2 += str(pos % 10 if pos % 10 != 0 else 10)
        print(col_header1)
        print(col_header2)
        print("-" * width)

    for idx, line in enumerate(lines, start=1):
        if labels:
            print(f"{idx:2d} {line}")
        else:
            print(line)


if __name__ == "__main__":
    n = 9
    print(f"\n=== n = {n} ===")
    print_pattern(n, labels=False)
