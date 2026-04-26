"""
ASCII из pyramid.json: вид сверху (план) — ось N↑, центр 5, четыре стороны Ло Шу;
дополнительно прямоугольная сетка операторов.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

# Порядок колонок в таблице (South … North слева направо)
SIDE_ORDER = ("South", "East", "West", "North")
COL_W = 7
NCOLS = 4
INNER_WIDTH = NCOLS * COL_W + (NCOLS + 1)
# Ширина блока плана и строки замыкания 0 (одинаковая)
PLAN_DISPLAY_WIDTH = max(INNER_WIDTH, 47)

_ARROW_SPLIT = re.compile(r"\s*(?:→|->|=>)\s*")
_SEGMENT_RE = re.compile(r"^([A-Za-z_]+)\(([^)]*)\)$")


def _repo_root() -> Path:
    return Path(__file__).resolve().parent


def load_onelaw(json_path: Path | None = None) -> dict:
    path = json_path or (_repo_root() / "pyramid.json")
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if "OneLaw" not in data:
        raise ValueError("Ожидается корневой ключ OneLaw в pyramid.json")
    return data["OneLaw"]


def _side_op_digits(side: dict) -> tuple[str, list[int]]:
    op = str(side.get("operator", side.get("op", "?")))
    digits = list(side.get("digits") or [])
    return op, digits


def format_expression(op: str, digits: list[int]) -> str:
    if len(digits) == 2:
        return f"{digits[0]}{op}{digits[1]}"
    if len(digits) == 1:
        return f"{digits[0]}"
    return "?"


def _side_expr(side_name: str, sides: dict) -> str:
    s = sides.get(side_name, {})
    op, digits = _side_op_digits(s)
    return format_expression(op, digits)


def format_plan_view(sides: dict) -> list[str]:
    """
    Вид сверху: север вверху экрана, центр площадки — 5 (вершина в проекции),
    на сторонах света — пары и операторы из matrix_lo_shu.sides.
    """
    n_ex = _side_expr("North", sides)
    e_ex = _side_expr("East", sides)
    s_ex = _side_expr("South", sides)
    w_ex = _side_expr("West", sides)

    w = PLAN_DISPLAY_WIDTH
    lines: list[str] = []

    def c(line: str) -> str:
        return line.center(w)

    lines.append(c("N  North  (-)"))
    lines.append(c(n_ex))
    lines.append(c("|"))
    arm = f"{w_ex}  ---  5  ---  {e_ex}"
    lines.append(c(arm))
    lines.append(c("|"))
    lines.append(c("S  South  (+)"))
    lines.append(c(s_ex))
    lines.append("")
    lines.append(c("W " + w_ex + "  < center >  " + e_ex + " E"))
    return lines


def format_operator_pyramid(sides: dict) -> list[str]:
    """
    Таблица 4×колонки: та же семантика, что у плана, но строки South…North слева направо
    (удобно читать выражения столбцами).
    """
    cols: list[tuple[str, str, str]] = []
    for name in SIDE_ORDER:
        s = sides.get(name, {})
        op, digits = _side_op_digits(s)
        expr = format_expression(op, digits)
        cols.append((name, op, expr))

    col_w = COL_W
    ncols = len(cols)
    inner_width = ncols * col_w + (ncols + 1)
    lines: list[str] = []

    def cent(s: str) -> str:
        return s.center(inner_width)

    lines.append(cent("5"))
    lines.append(cent("|"))

    top = "+" + "+".join("-" * col_w for _ in range(ncols)) + "+"
    lines.append(cent(top))

    row_empty = "|" + "|".join(" " * col_w for _ in range(ncols)) + "|"
    lines.append(cent(row_empty))

    cells_ops = [c[1].center(col_w) for c in cols]
    lines.append(cent("|" + "|".join(cells_ops) + "|"))

    cells_expr = [c[2].center(col_w) for c in cols]
    lines.append(cent("|" + "|".join(cells_expr) + "|"))

    lines.append(cent(row_empty))
    lines.append(cent(top))

    label_cells = [c[0][:6].center(col_w) for c in cols]
    lines.append(cent("|" + "|".join(label_cells) + "|"))

    return lines


def _format_cycle_fallback(sides: dict) -> str:
    """Если sequence пуст или не распарсился — фиксированный порядок сторон."""
    parts: list[str] = ["0"]
    for name in ("South", "East"):
        s = sides.get(name, {})
        op, d = _side_op_digits(s)
        if len(d) == 2:
            parts.append(f"({d[0]}{op}{d[1]})")
    parts.append("5")
    for name in ("West", "North"):
        s = sides.get(name, {})
        op, d = _side_op_digits(s)
        if len(d) == 2:
            parts.append(f"({d[0]}{op}{d[1]})")
    parts.append("0")
    return " -> ".join(parts)


def _format_cycle_parsed(sequence: str, sides: dict) -> str:
    """Развёртка строго по шагам full_cycle.sequence; операторы и операнды из sides."""
    parts: list[str] = []
    for seg in _ARROW_SPLIT.split(sequence.strip()):
        seg = seg.strip()
        if not seg:
            continue
        if seg == "0":
            parts.append("0")
            continue
        compact = re.sub(r"\s+", "", seg)
        m = _SEGMENT_RE.match(compact)
        if not m:
            raise ValueError(f"Неизвестный фрагмент цикла: {seg!r}")
        name, inner = m.group(1), m.group(2)
        if name == "Center":
            nums = [p.strip() for p in inner.split(",") if p.strip()]
            if len(nums) != 1:
                raise ValueError(f"Center должен иметь одну цифру: {seg!r}")
            parts.append(nums[0])
            continue
        if name not in sides:
            raise ValueError(f"Неизвестная сторона в цикле: {name}")
        op, d = _side_op_digits(sides[name])
        if len(d) == 2:
            parts.append(f"({d[0]}{op}{d[1]})")
        elif len(d) == 1:
            parts.append(f"({d[0]})")
        else:
            parts.append("(?)")
    return " -> ".join(parts)


def format_cycle_strict(sequence: str, sides: dict) -> str:
    """
    Одна строка развёртки в порядке full_cycle.sequence.
    При пустом или невалидном sequence — запасной порядок South, East, 5, West, North.
    """
    if not sequence or not sequence.strip():
        return _format_cycle_fallback(sides)
    try:
        return _format_cycle_parsed(sequence, sides)
    except ValueError:
        return _format_cycle_fallback(sides)


def format_lo_shu_compact(grid: list[list[int]]) -> str:
    lines = ["  Ло Шу (позиции в плоскости):"]
    for row in grid:
        lines.append("    " + "  ".join(f"{x}" for x in row))
    return "\n".join(lines)


def _validate_grid(grid: list[list[int]]) -> None:
    if len(grid) != 3 or any(len(row) != 3 for row in grid):
        raise ValueError("matrix_lo_shu.grid должен быть 3×3")
    for row in grid:
        for x in row:
            if not isinstance(x, int):
                raise ValueError("В grid ожидаются целые числа")


def run(json_path: Path | None = None, *, show_grid: bool = True) -> None:
    ol = load_onelaw(json_path)
    meta = ol.get("meta", {})
    matrix = ol.get("matrix_lo_shu", {})
    grid = matrix.get("grid")
    sides = matrix.get("sides") or {}
    fc = ol.get("full_cycle", {})
    sequence = fc.get("sequence", "")

    if not grid:
        raise ValueError("В JSON не хватает matrix_lo_shu.grid")
    _validate_grid(grid)
    for name in SIDE_ORDER:
        if name not in sides:
            raise ValueError(f"В matrix_lo_shu.sides нет стороны {name}")

    print(f"=== {meta.get('title', 'OneLaw')} (v {meta.get('version', '?')}) ===\n")

    if show_grid:
        print(format_lo_shu_compact(grid))
        print()

    print("--- Вид сверху (план): N вверх, центр 5, стороны света ---\n")
    for line in format_plan_view(sides):
        print(line)
    print()

    print("--- Та же логика в прямоугольной сетке (South … North слева направо) ---\n")
    for line in format_operator_pyramid(sides):
        print(line)
    print()

    print("--- Замыкание цикла (∅) ---\n")
    print("0".center(PLAN_DISPLAY_WIDTH))
    print()

    print("--- Строгая последовательность (как в full_cycle, с операторами) ---")
    if sequence:
        print(f"  JSON: {sequence}")
    print(f"  Развёртка: {format_cycle_strict(sequence, sides)}")
    print()


def main() -> None:
    p = argparse.ArgumentParser(description="Вершина 5 и четыре операции из pyramid.json")
    p.add_argument("--json", type=Path, default=None, help="Путь к pyramid.json")
    p.add_argument("--no-grid", action="store_true", help="Не печатать таблицу 3×3")
    args = p.parse_args()
    run(json_path=args.json, show_grid=not args.no_grid)


if __name__ == "__main__":
    main()
