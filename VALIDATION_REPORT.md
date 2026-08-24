# Validation report — v2.0.0

**Validation date:** 2026-08-24

## Completed checks

- Scenario rebuild script executed successfully with deterministic seed `20260819`.
- Repository preflight, including metadata, license notices, source data and `docs/.nojekyll`: **PASS**.
- Python syntax compilation (`app.py`, `scripts/`, `tests/`): **PASS**.
- Release test suite: **9 passed** (four model tests and five static-integrity tests).
- JSON parsing for `.zenodo.json`, `codemeta.json`, `datacite.json` and `ro-crate-metadata.json`: **PASS**.
- YAML parsing for `CITATION.cff`: **PASS**.
- ORCID, declared affiliation, repository URL and GitHub Pages URL consistency: **PASS**.
- Layered license policy and third-party notices: **PASS**.
- Deterministic release manifest and SHA-256 inventory verification: **PASS**.
- Heuristic scan for embedded local paths, common secret patterns and credentials: **no findings**.
- Master XLSX created with `artifact_tool`; key dashboard and formula ranges inspected; formula-error scan returned zero matches.
- Dashboard XLSX was rendered for visual inspection before export.
- Static viewer is self-contained (embedded Plotly) and references release data files by relative paths.

## Environment qualification

The build container used for this release did not have `shiny` preinstalled, so a live import/server smoke test was not executed in that container. Runtime dependencies and version bounds are declared in `requirements.txt`, `pyproject.toml`, and `Dockerfile`; Python syntax, preflight, release-inventory and data/model tests passed independently. GitHub Actions will repeat these checks on every push and pull request.

## Data-quality invariant

Peru's 2025 overall score (5.88) is treated as observed/secondary-replicated EIU data. Peru's five 2025 category values are explicitly flagged as a modeled latent calibration and must not be cited as official EIU sub-pillar values.
