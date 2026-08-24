# Release notes — v2.0.0 (2026-08-19)

## Release scientific scope

This release fuses the historical infographic/viewer and the prior 2030 prospective viewer into one portable research package.

### Data update
- Historical layer extended through 2025.
- Peru 2025 overall Democracy Index: 5.88, hybrid regime; rank 76 in a secondary cross-country replication of EIU rankings.
- Latin America and the Caribbean 2025: 5.71; world: 5.19.
- Peru 2025 sub-pillar values are explicitly tagged as a latent calibration, not as official EIU values.

### Prospective update
- Previous scenario set reduced to three auditable scenarios: institutional recovery, hybrid continuity, restrictive/securitised drift.
- 2026 shocks conditioned on post-election evidence through 2026-08-17, including JNE, OAS and the EU EOM final report, plus newswire and academic/expert evidence.
- Monte Carlo sensitivity envelope: 10,000 simulations/scenario, deterministic seed 20260819; p10–p90 is sensitivity, not event probability.

### Portable/repository-grade delivery
- Shiny for Python application (`app.py`).
- Self-contained Plotly static viewer (`docs/index.html`).
- CSV analytical layer + master XLSX.
- Dockerfile / docker-compose.
- CITATION.cff, CodeMeta, Zenodo metadata, DataCite metadata and RO-Crate metadata.
- Tests, preflight, reproducibility script, checksums and release manifest.

### Release metadata and licensing
- Author ORCID: `0000-0002-7913-214X`.
- Affiliation normalized from the author's public academic profile.
- GitHub repository and GitHub Pages URLs propagated across citation, CodeMeta, DataCite and RO-Crate metadata.
- Layered licensing: MIT for original code; CC BY 4.0 for original documentation and curated/derived contributions; third-party inputs retain their original terms.
- Added `docs/.nojekyll` for direct GitHub Pages publication from `/docs`.
