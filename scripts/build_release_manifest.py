#!/usr/bin/env python3
"""Build or verify the deterministic SHA-256 release inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
MANIFEST_PATH = BASE / "RELEASE_MANIFEST.json"
CHECKSUM_PATH = BASE / "SHA256SUMS.txt"
EXCLUDED_FILES = {"RELEASE_MANIFEST.json", "SHA256SUMS.txt"}
EXCLUDED_DIRS = {".git", ".venv", ".pytest_cache", "__pycache__", "_exports"}


def payload_files() -> list[Path]:
    files = []
    for path in BASE.rglob("*"):
        rel = path.relative_to(BASE)
        if not path.is_file():
            continue
        if rel.as_posix() in EXCLUDED_FILES:
            continue
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        files.append(path)
    return sorted(files, key=lambda p: p.relative_to(BASE).as_posix())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def expected_outputs() -> tuple[str, str]:
    entries = []
    checksum_lines = []
    for path in payload_files():
        rel = path.relative_to(BASE).as_posix()
        digest = sha256(path)
        entries.append({"path": rel, "bytes": path.stat().st_size, "sha256": digest})
        checksum_lines.append(f"{digest}  {rel}")

    manifest = {
        "project": "Visor Integrado de Democracia del Perú 2020–2030",
        "version": "2.1.0-rc.1",
        "release_date": "2026-08-25",
        "manifest_revision_date": "2026-08-25",
        "author": {
            "name": "Magdiel Torres Vanegas",
            "orcid": "https://orcid.org/0000-0002-7913-214X",
        },
        "hash_algorithm": "SHA-256",
        "inventory_excludes": sorted(EXCLUDED_FILES),
        "file_count": len(entries),
        "total_bytes": sum(item["bytes"] for item in entries),
        "files": entries,
    }
    manifest_text = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    checksum_text = "\n".join(checksum_lines) + "\n"
    return manifest_text, checksum_text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify without writing")
    args = parser.parse_args()
    manifest_text, checksum_text = expected_outputs()
    if args.check:
        valid = True
        for path, expected in ((MANIFEST_PATH, manifest_text), (CHECKSUM_PATH, checksum_text)):
            if not path.is_file() or path.read_text(encoding="utf-8") != expected:
                print(f"OUTDATED: {path.name}")
                valid = False
        if valid:
            print("RELEASE MANIFEST OK")
            return 0
        return 1
    MANIFEST_PATH.write_text(manifest_text, encoding="utf-8")
    CHECKSUM_PATH.write_text(checksum_text, encoding="utf-8")
    print(f"WROTE {MANIFEST_PATH.name} and {CHECKSUM_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
