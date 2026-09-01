#!/usr/bin/env python3
"""Build or verify the deterministic SHA-256 release inventory.

The inventory files themselves are written and verified as raw UTF-8 bytes.
This intentionally bypasses platform newline translation so Windows and Linux
produce byte-identical RELEASE_MANIFEST.json and SHA256SUMS.txt files.
"""

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
        "version": "2.1.0",
        "release_date": "2026-08-31",
        "manifest_revision_date": "2026-08-31",
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


def expected_output_bytes() -> tuple[bytes, bytes]:
    manifest_text, checksum_text = expected_outputs()
    return manifest_text.encode("utf-8"), checksum_text.encode("utf-8")


def _is_canonical_text_bytes(raw: bytes) -> bool:
    return not raw.startswith(b"\xef\xbb\xbf") and b"\r" not in raw


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify exact bytes without writing")
    args = parser.parse_args()
    manifest_bytes, checksum_bytes = expected_output_bytes()
    outputs = ((MANIFEST_PATH, manifest_bytes), (CHECKSUM_PATH, checksum_bytes))

    if args.check:
        valid = True
        for path, expected in outputs:
            if not path.is_file():
                print(f"MISSING: {path.name}")
                valid = False
                continue
            actual = path.read_bytes()
            if actual != expected:
                print(f"OUTDATED: {path.name}")
                valid = False
            if not _is_canonical_text_bytes(actual):
                print(f"NONCANONICAL_TEXT: {path.name}")
                valid = False
        if valid:
            print("RELEASE MANIFEST OK")
            return 0
        return 1

    # write_bytes is deliberate: Path.write_text/newline handling is platform
    # dependent on Windows and previously introduced CRLF after normalization.
    MANIFEST_PATH.write_bytes(manifest_bytes)
    CHECKSUM_PATH.write_bytes(checksum_bytes)
    print(f"WROTE {MANIFEST_PATH.name} and {CHECKSUM_PATH.name} as UTF-8/LF bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
