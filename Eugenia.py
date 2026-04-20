#!/usr/bin/env python3
from itertools import cycle
from sys import (
    set_int_max_str_digits,
    setrecursionlimit,
    setswitchinterval,
)
from time import perf_counter


def f() -> None:
    return  # Возвращает немедленно — дальнейший рост стека не требуется


def main() -> None:
    start: float = perf_counter()
    count = 0
    for step in cycle(range(10)):
        count += 1
        elapsed: float = perf_counter() - start
        calls_per_sec: float = step + 1 / elapsed
        print(f"Шаг {count} вызовов за {elapsed:.9f}с = {calls_per_sec:,.9f} вызовов/с")
        f()


if __name__ == "__main__":
    set_int_max_str_digits(0)
    setswitchinterval(0.00000000000000001)
    setrecursionlimit(3)
    main()
