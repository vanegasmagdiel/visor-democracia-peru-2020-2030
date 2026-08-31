# Windows manifest hotfix — v2.1.0

**Date:** 2026-08-31  
**Scope:** publication pipeline only

## Observed failure

The Windows validation pipeline correctly rebuilt `docs/index.html` using the exact locked runtime, but the packaged `RELEASE_MANIFEST.json` and `SHA256SUMS.txt` still described the pre-rebuild payload. Therefore `test_release_inventory_is_current` failed after the deterministic rebuild even though the scientific build itself had succeeded.

## Root cause

`Test-And-Build` executed `build_static_viewer.py` before `pytest`, while the release inventory was only checked after tests and was not regenerated after deterministic output files changed. The failure was therefore an ordering/inventory-staleness defect, not a scientific-model defect.

## Correction

The publisher now regenerates `RELEASE_MANIFEST.json` and `SHA256SUMS.txt` after all deterministic rebuild steps and before `pytest`. The static publisher audit also asserts the required ordering:

`build_static_viewer -> build_release_manifest (write) -> pytest -> build_release_manifest --check`

The inventory files themselves remain excluded from their own payload inventory. `.venv`, caches and Git metadata remain excluded.

## Release effect

No dataset, scenario parameter, seed, PRISMA decision, figure semantics or scientific result is changed by this hotfix. It closes **B-P0-09 — post-rebuild manifest regeneration**.
