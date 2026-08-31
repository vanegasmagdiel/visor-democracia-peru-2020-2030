#!/usr/bin/env python3
"""Fail when editorial artifacts or release dependencies enter the software object."""

from __future__ import annotations

import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".bat", ".cff", ".csv", ".json", ".md", ".ps1", ".py", ".sh",
    ".toml", ".txt", ".yaml", ".yml",
}
JOURNAL_TOKEN = "sci" + "endo"
JOURNAL_TOKEN_ACCENTED = "sci" + "éndo"
ARTICLE_GATE = "article_" + "final_reference_integration_ready"
PROHIBITED_PATH_PARTS = {"manu" + "script"}
PROHIBITED_FILENAMES = {
    "pendientes_" + "externos.md",
}


def audit() -> list[str]:
    errors: list[str] = []
    for path in BASE.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(BASE)
        rel_lower = rel.as_posix().lower()
        if any(part.lower() in PROHIBITED_PATH_PARTS for part in rel.parts):
            errors.append(f"prohibited release path: {rel.as_posix()}")
        if path.name.lower() in PROHIBITED_FILENAMES:
            errors.append(f"prohibited editorial control file: {rel.as_posix()}")
        if "articulo_original" in rel_lower or "article_original" in rel_lower:
            errors.append(f"prohibited manuscript artifact: {rel.as_posix()}")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8-sig").lower()
        except UnicodeDecodeError:
            continue
        if JOURNAL_TOKEN in text or JOURNAL_TOKEN_ACCENTED in text:
            errors.append(f"journal-specific token in: {rel.as_posix()}")
        if ARTICLE_GATE in text:
            errors.append(f"article-dependent release gate in: {rel.as_posix()}")

    manifest = json.loads((BASE / "data/prisma_phase8/phase8_manifest.json").read_text(encoding="utf-8"))
    gate = manifest["publication_gate"]
    required = {
        "fulltext_complete",
        "final_prisma_ready",
        "release_scientific_validation_ready",
        "dependency_lock_ready",
        "release_gate_decoupled",
        "phase8_canonical_narrative",
        "metadata_method_classification",
    }
    for key in required:
        if gate.get(key) is not True:
            errors.append(f"technical release gate not true: {key}")
    if gate.get("osf_sync_required") is not False:
        errors.append("OSF must remain optional")
    return errors


def main() -> int:
    errors = audit()
    if errors:
        print("RELEASE INDEPENDENCE AUDIT FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("RELEASE INDEPENDENCE AUDIT OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
