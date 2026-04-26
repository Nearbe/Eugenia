#!/usr/bin/env python3
"""Выводит все функции из каждого файла src/core/."""

import ast
import sys
from pathlib import Path


def get_functions(file_path: Path) -> list[tuple[str, int]]:
    """Вернуть список (имя_функции, номер_строки) из файла."""
    try:
        text = file_path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(file_path))
    except (SyntaxError, UnicodeDecodeError):
        return []

    results = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            results.append((node.name, node.lineno))
    return results


def main() -> None:
    core_dir = Path(__file__).parent / "src" / "core"
    if not core_dir.is_dir():
        core_dir = Path("src/core")

    for py_file in sorted(core_dir.glob("*.py")):
        if py_file.name == "__init__.py":
            continue
        funcs = get_functions(py_file)
        if not funcs:
            print(f"\n{py_file.name}: (нет функций)")
        else:
            print(f"\n{py_file.name} ({len(funcs)} функций):")
            for name, line in funcs:
                print(f"  {line:>3}: {name}")


if __name__ == "__main__":
    main()
