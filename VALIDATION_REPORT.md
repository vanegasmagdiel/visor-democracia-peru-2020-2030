# Validation report — v2.1.0-rc.1

**Validation date:** 2026-08-25
**Publication status:** review candidate; no final tag or new Zenodo DOI.

## Scientific and data controls

- Deterministic rebuild with seed `20260825`: **PASS**.
- 10,000 latent 2025 dimensional vectors, each with exact mean `5.88`:
  **PASS**.
- Separation between `secondary_reported_aggregate`, latent dimensional values
  and simulated scenarios: **PASS**.
- Thirty scenario parameters with ordered plausible ranges and complete
  evidence/translation fields: **PASS**.
- Evidence register without numeric weights and with
  `computational_use=false`: **PASS**.
- Three-scenario ordering, 0–10 bounds and p10 ≤ p50 ≤ p90 invariants: **PASS**.
- Sensitivity labels explicitly reject confidence-interval and
  scenario-probability interpretations: **PASS**.

## Product consistency

- Scientific preflight: **PASS**.
- Python syntax compilation for application, scripts and tests: **PASS**.
- Test suite after final manifest generation: **15 tests passed**.
- Shiny live server smoke test on local HTTP endpoint: **PASS**.
- Static self-contained viewer rebuild: **PASS**.
- Public download synchronization under `docs/data`: **PASS**.
- JSON/CFF identity, ORCID, affiliation, repository and version consistency:
  **PASS**.
- `.nojekyll`, GitHub Pages source and required publication files: **PASS**.
- Heuristic credential and machine-path scan: **PASS; no findings**.

## XLSX quality assurance

- Integral workbook rebuilt with `artifact_tool`: **PASS**.
- Fourteen sheets produced, including dashboard, latent-anchor audit, parameter
  elicitation, evidence, aggregate/dimensional sensitivity, statuses,
  methodology and data dictionary.
- Every sheet rendered at least once for visual review: **PASS**.
- Dashboard, anchor, parameter and 2030 summary renders manually inspected:
  **PASS**.
- Formula-error scan (`#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#N/A`):
  **zero matches**.

## Publication automation

- BAT wrapper resolves the PowerShell publisher by its own directory: **PASS**.
- PowerShell delimiter/structure audit: **PASS**.
- Static policy tests confirm explicit `-PublishRelease` switch, exact final
  confirmation phrase, RC metadata guard and OSF whitelist: **PASS**.
- ZIP-root discovery is recursive and requires `pyproject.toml`,
  `docs/index.html` and the v2.1 model configuration, eliminating the prior
  fixed-path failure.
- Git identity uses the authenticated GitHub user’s noreply address,
  eliminating the prior blank-email prompt.
- Git remote is forced to SSH, eliminating the prior HTTPS OAuth workflow-scope
  rejection.
- Native BAT execution must occur on Windows; in the build environment its
  equivalent gates, model rebuild and tests were executed directly.

## External-platform qualification

- GitHub candidate publication is limited to a branch and draft PR.
- GitHub Pages remains tied to `main/docs`; the stable page is not replaced by
  an unreviewed candidate.
- The authenticated OSF dashboard contained no project and redirected new
  research-material storage to external repositories. Therefore no OSF write
  was attempted. The BAT can synchronize only a preexisting OSF project GUID
  and never uploads the primary ZIP.
- Zenodo v2.0.0 and DOI `10.5281/zenodo.22080541` remain immutable. The concept
  DOI is `10.5281/zenodo.22080540`.

## Deferred gate

Phase 8 will add the PRISMA-agent corpus and screening outputs. Phases 9–11 and
an explicit GO are required before removing the RC label, merging the PR,
creating tag `v2.1.0`, creating a GitHub Release or minting a new Zenodo DOI.
