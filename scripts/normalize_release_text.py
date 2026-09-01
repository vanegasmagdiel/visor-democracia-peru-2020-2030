#!/usr/bin/env python3
"""Normalize release text payloads to UTF-8 without BOM and LF endings."""
from __future__ import annotations
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".bat", ".cff", ".css", ".csv", ".html", ".js", ".json", ".md",
    ".ps1", ".py", ".rst", ".sh", ".svg", ".toml", ".txt", ".xml",
    ".yaml", ".yml",
}
TEXT_NAMES = {".gitattributes", ".gitignore"}
SKIP_DIRS = {".git", ".venv", ".pytest_cache", "__pycache__", "_exports"}


def candidates():
    for path in BASE.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(BASE)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.name in TEXT_NAMES or path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def normalize(path: Path) -> bool:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return False
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    if raw != normalized:
        path.write_bytes(normalized)
        return True
    return False


def main() -> int:
    changed = [p.relative_to(BASE).as_posix() for p in candidates() if normalize(p)]
    print(f"TEXT NORMALIZATION OK ({len(changed)} file(s) normalized)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
