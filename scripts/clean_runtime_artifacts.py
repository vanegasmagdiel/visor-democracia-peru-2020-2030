#!/usr/bin/env python3
"""Remove transient runtime artifacts before release inventory generation."""
from __future__ import annotations
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SKIP = {".git", ".venv"}
DIR_NAMES = {"__pycache__", ".pytest_cache"}
FILE_NAMES = {".DS_Store", "Thumbs.db"}


def main() -> int:
    removed = 0
    for path in sorted(BASE.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        rel = path.relative_to(BASE)
        if any(part in SKIP for part in rel.parts):
            continue
        if path.is_dir() and path.name in DIR_NAMES:
            shutil.rmtree(path, ignore_errors=True)
            removed += 1
        elif path.is_file() and (path.name in FILE_NAMES or path.suffix.lower() == ".pyc"):
            path.unlink(missing_ok=True)
            removed += 1
    print(f"RUNTIME CLEANUP OK ({removed} artifact(s) removed)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
