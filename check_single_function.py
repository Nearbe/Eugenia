#!/usr/bin/env python3
"""Проверка src/core/: файлы с >1 функции."""

import sys
from pathlib import Path


def count_functions(file_path: Path) -> int:
    """Считать количество функций (def) в файле."""
    count = 0
    try:
        text = file_path.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.lstrip()
            if stripped.startswith("def ") or stripped.startswith("async def "):
                count += 1
    except Exception:
        pass
    return count


def main() -> None:
    core_dir = Path(__file__).parent / "core"
    if not core_dir.is_dir():
        core_dir = Path("src/core")

    violations = []
    for py_file in sorted(core_dir.glob("*.py")):
        if py_file.name == "__init__.py":
            continue
        n = count_functions(py_file)
        if n > 1:
            violations.append((py_file, n))

    if violations:
        print(f"Файлов с >1 функции: {len(violations)}\n")
        for path, n in violations:
            print(f"  {path.name}: {n} функций")
    else:
        print("OK: все файлы содержат по 1 функции.")


if __name__ == "__main__":
    main()
