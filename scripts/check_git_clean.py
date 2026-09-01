#!/usr/bin/env python3
"""Fail CI when deterministic rebuild leaves tracked or untracked changes."""
from __future__ import annotations
import subprocess
import sys


def main() -> int:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        text=True, capture_output=True, check=False,
    )
    if result.returncode != 0:
        print(result.stderr.strip())
        return result.returncode
    dirty = result.stdout.strip()
    if dirty:
        print("GIT CLEAN CHECK FAIL")
        print(dirty)
        return 1
    print("GIT CLEAN CHECK OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())
