#!/usr/bin/env python3
"""Fail on common credentials or machine-specific paths in release payloads."""

from __future__ import annotations

import re
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
TEXT_EXTENSIONS = {
    ".bat", ".cff", ".csv", ".html", ".json", ".md", ".ps1", ".py",
    ".sh", ".toml", ".txt", ".yaml", ".yml",
}
EXCLUDED_DIRS = {".git", ".venv", ".pytest_cache", "__pycache__"}
PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:ghp|gho|ghu|ghs|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "embedded bearer token": re.compile(r"Authorization\s*[:=]\s*Bearer\s+[A-Za-z0-9._~-]{20,}", re.I),
    "embedded password": re.compile(r"(?:password|passwd|pwd)\s*[:=]\s*[\"'][^\"']{6,}[\"']", re.I),
    "Windows user path": re.compile(r"\b[A-Za-z]:\\Users\\[^\\\s]+\\", re.I),
    "Unix home path": re.compile(r"/(?:home|Users)/[^/\s]+/"),
}


def main() -> int:
    findings: list[str] = []
    for path in sorted(BASE.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        rel = path.relative_to(BASE)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{rel.as_posix()}:{line}: {label}")
    if findings:
        print("SECRET SCAN FAIL")
        print("\n".join(f"- {item}" for item in findings))
        return 1
    print("SECRET SCAN OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
