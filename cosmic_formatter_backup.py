# ╔════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║─Эта часть кода не должна изменяться─────────────────────────────────────────────────────────────║
# ║─Она олицетворяет бесконечность через вечность───────────────────────────────────────────────────║
# ║─Или же пустота, что по-сути является 0 или точкой начала Вселенной─────────────────────────────║
# ║─Её присутствие в коде это буквально ручка которая дотягивается до старта───────────────────────║
# ║─Когда-то вся Вселенная выглядела именно так────────────────────────────────────────────────────║
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════╝
#!/usr/bin/env python3
"""
Cosmic Formatter — universal code block decorator.

Wraps code blocks in ASCII cosmic frames that look the same everywhere,
across all languages, without affecting execution.

Rules:
  1. Top border:     # ╔ + N '=' + ╗
  2. Comment lines:  # ║─text─║  (philosophical / descriptive text)
  3. Divider:        # ║─N*'─'─║
  4. Code line:      <code>#─N*'─'─║>  (code + decorative comment)
  5. Bottom border:  # ╚ + N '=' + ╝
  6. Frame width:   N = 100 characters between ║ markers
  7. Every line contains '#'
  8. Decoration length is synchronized across all lines
"""

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

FRAME_WIDTH: int = 100
TOP_BORDER: str = f"# ╔{'═' * FRAME_WIDTH}╗"
BOTTOM_BORDER: str = f"# ╚{'═' * FRAME_WIDTH}╝"
DIVIDER: str = f"# ║{'─' * FRAME_WIDTH}║"


@dataclass
class CommentBlock:
    lines: list[str] = field(default_factory=list)

    def to_lines(self) -> list[str]:
        result: list[str] = []
        for text in self.lines:
            prefix = "║─"
            suffix_base = "─║"
            available = FRAME_WIDTH - len(prefix) - len(suffix_base)
            text_len = min(len(text), available)
            text = text[:text_len]
            line = f"# {prefix}{text}{'─' * (available - len(text))}{suffix_base}"
            result.append(line)
        return result


@dataclass
class CodeLine:
    code: str

    def to_line(self) -> str:
        code_part = self.code
        decoration_prefix = "#─"
        suffix = "║"
        available = FRAME_WIDTH - len(code_part)
        if available < 0:
            # Truncate with '......' instead of '…' to avoid Python syntax issues
            code_part = code_part[:FRAME_WIDTH - 6] + "......"
            available = FRAME_WIDTH - len(code_part)
        line = f"{code_part}{decoration_prefix}{'─' * available}{suffix}"
        return line


@dataclass
class CosmicBlock:
    comments: CommentBlock = field(default_factory=CommentBlock)
    code_lines: list[CodeLine] = field(default_factory=list)

    def to_lines(self) -> list[str]:
        result: list[str] = [TOP_BORDER]
        result.extend(self.comments.to_lines())
        result.append(DIVIDER)
        for cl in self.code_lines:
            result.append(cl.to_line())
        result.append(BOTTOM_BORDER)
        return result


PHILOSOPHY: list[str] = [
    "Эта часть кода не должна изменяться",
    "Она олицетворяет бесконечность через вечность",
    "Или же пустота, что по-сути является 0 или точкой начала Вселенной",
    "Её присутствие в коде это буквально ручка которая дотягивается до старта",
    "Когда-то вся Вселенная выглядела именно так",
]

COSMIC_START = re.compile(r'^#\s*╔')
COSMIC_END = re.compile(r'^#\s*╚')
COSMIC_FRAME = re.compile(r'^#.*║.*║.*$')


def is_cosmic_block_start(line: str) -> bool:
    return bool(COSMIC_START.match(line))


def is_cosmic_block_end(line: str) -> bool:
    return bool(COSMIC_END.match(line))


def is_cosmic_comment(line: str) -> bool:
    return bool(re.match(r'^#\s*║─([^─].*?)─║\s*$', line))


def is_cosmic_divider(line: str) -> bool:
    return bool(re.match(r'^#\s*║─+║\s*$', line))


def is_cosmic_code_line(line: str) -> str | None:
    if re.match(r'^#\s*║', line):
        return None
    m = re.match(r'^([^\n#]+?)\s*#\s*─+║\s*$', line)
    if m:
        code = m.group(1).rstrip()
        if code and not COSMIC_FRAME.match(code):
            return code
    return None


def extract_cosmic_blocks(lines: list[str]) -> list[CosmicBlock]:
    blocks: list[CosmicBlock] = []
    i = 0
    while i < len(lines):
        if is_cosmic_block_start(lines[i]):
            block = CosmicBlock()
            i += 1
            while i < len(lines) and is_cosmic_comment(lines[i]) and not is_cosmic_divider(lines[i]):
                m = re.match(r'^#\s*║─(.+?)─║\s*$', lines[i])
                if m:
                    block.comments.lines.append(m.group(1))
                i += 1
            if i < len(lines) and is_cosmic_divider(lines[i]):
                i += 1
            while i < len(lines):
                if is_cosmic_block_end(lines[i]):
                    break
                code = is_cosmic_code_line(lines[i])
                if code is not None:
                    block.code_lines.append(CodeLine(code))
                i += 1
            if i < len(lines):
                blocks.append(block)
        i += 1
    return blocks


def generate_block(code_lines: list[str], comments: Optional[list[str]] = None) -> CosmicBlock:
    block = CosmicBlock()
    if comments:
        block.comments.lines = comments
    else:
        n = min(len(code_lines), len(PHILOSOPHY))
        block.comments.lines = PHILOSOPHY[:n]
    block.code_lines = [CodeLine(line) for line in code_lines]
    return block


def format_cosmic_block(block: CosmicBlock) -> str:
    return '\n'.join(block.to_lines())


def format_file(path: Path) -> str:
    content = path.read_text(encoding='utf-8')
    lines = content.split('\n')
    while lines and not lines[-1].strip():
        lines.pop()
    block = generate_block(lines)
    return format_cosmic_block(block)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: cosmic_formatter.py <file_or_directory>...")
        print("  Formats cosmic frame blocks in the given files.")
        print("  Pass '-' for stdin.")
        return 1

    for target in sys.argv[1:]:
        path = Path(target)

        if target == '-':
            content = sys.stdin.read()
            lines = content.split('\n')
            while lines and not lines[-1].strip():
                lines.pop()
            if lines:
                block = generate_block(lines)
                print(format_cosmic_block(block), end='')
            else:
                print(content, end='')
        elif path.is_dir():
            for file_path in path.rglob('*'):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    new_content = format_file(file_path)
                    file_path.write_text(new_content, encoding='utf-8')
                    print(f"Formatted: {file_path}")
        elif path.is_file():
            new_content = format_file(path)
            path.write_text(new_content, encoding='utf-8')
            print(f"Formatted: {path}")
        else:
            print(f"Not found: {target}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
