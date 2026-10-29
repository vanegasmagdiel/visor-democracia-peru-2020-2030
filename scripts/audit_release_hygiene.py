#!/usr/bin/env python3
"""Audit release payload hygiene and separation from editorial/attempt artifacts."""
from __future__ import annotations
import re
import hashlib
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "_exports"}
RUNTIME_DIRS = {".pytest_cache", "__pycache__"}
FORBIDDEN_NAMES = {".DS_Store", "Thumbs.db"}
FORBIDDEN_PATH_SNIPPETS = {
    "data/prisma_phase8/archive/pre_fulltext",
    "manuscript/",
}
FORBIDDEN_NAME_PATTERNS = [
    re.compile(r"hotfix", re.I),
    re.compile(r"pre_release_fixes", re.I),
    re.compile(r"rc5_closure_report", re.I),
    re.compile(r"windows_manifest", re.I),
    re.compile(r"dry_run_report", re.I),
]
FROZEN_CANONICAL_ARCHIVES = {'docs/downloads/archivo_zenodo_v210.zip': 'e4487348d3a367105b44c78a30066ce9e074306c25ff6c8c42eeadd2e21fb964', 'docs/downloads/base_cientifica_v210.zip': 'c8a07cc4538587592e41dca75f8ad6fa12541370465748a60e80e377e5b61439'}
FORBIDDEN_ARCHIVE_SUFFIXES = {".zip", ".sha256"}


def audit() -> list[str]:
    errors: list[str] = []
    for path in BASE.rglob("*"):
        rel = path.relative_to(BASE)
        rel_posix = rel.as_posix()
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if any(part in RUNTIME_DIRS for part in rel.parts):
            continue
        if path.is_dir():
            continue
        if path.name in FORBIDDEN_NAMES:
            errors.append(f"OS/editor residue: {rel_posix}")
        if any(snippet in rel_posix.lower() for snippet in FORBIDDEN_PATH_SNIPPETS):
            errors.append(f"obsolete/intermediate payload path: {rel_posix}")
        if any(pattern.search(path.name) for pattern in FORBIDDEN_NAME_PATTERNS):
            errors.append(f"attempt-specific residual file: {rel_posix}")
        if rel_posix in FROZEN_CANONICAL_ARCHIVES:
            if hashlib.sha256(path.read_bytes()).hexdigest() != FROZEN_CANONICAL_ARCHIVES[rel_posix]:
                errors.append(f"frozen source archive integrity mismatch: {rel_posix}")
        elif path.suffix.lower() in FORBIDDEN_ARCHIVE_SUFFIXES:
            errors.append(f"nested package/checksum inside release object: {rel_posix}")
    return sorted(set(errors))


def main() -> int:
    errors = audit()
    if errors:
        print("RELEASE HYGIENE AUDIT FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("RELEASE HYGIENE AUDIT OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())
