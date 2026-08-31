# Validation report — v2.1.0-rc.5

**Validation date:** 2026-08-31
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
- Test suite after final manifest generation: **PASS — 27/27**.
- Shiny live server smoke test on local HTTP endpoint: **PASS**.
- Static self-contained viewer rebuild: **PASS**.
- Public download synchronization under `docs/data`: **PASS**.
- JSON/CFF identity, ORCID, affiliation, repository and version consistency:
  **PASS**.
- `.nojekyll`, GitHub Pages source and required publication files: **PASS**.
- Heuristic credential and machine-path scan: **PASS; no findings**.

## Phase 8 PRISMA controls

- Source files preserved with SHA-256: **PASS**.
- PRISMA arithmetic `767 − 3 − 116 = 648` and `648 − 576 = 72`: **PASS**.
- Exclusion reasons `453 + 122 + 1 = 576`: **PASS**.
- Record-level full-text decisions: `72/72`: **PASS**.
- Retrieval arithmetic `42 + 30 = 72`: **PASS**.
- Eligibility arithmetic `29 + 13 = 42`: **PASS**.
- Final included RIS and CSV identity agreement `29/29`: **PASS**.
- Final PRISMA figure labels the corpus as support for an original article: **PASS**.
- Full-text eligibility and final inclusion: **COMPLETE**.

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
- Audit/publication control workbook: **10 sheets rendered and visually reviewed;
  formula scan with zero matches**.

## Publication automation

- BAT wrapper resolves the PowerShell publisher by its own directory: **PASS**.
- PowerShell delimiter/structure audit: **PASS**.
- Static policy tests confirm `-DryRun`, explicit `-PublishRelease`, exact final
  confirmation phrase, RC metadata guard and OSF whitelist: **PASS**.
- ZIP-root discovery is recursive and requires `pyproject.toml`,
  `docs/index.html` and the v2.1 model configuration, eliminating the prior
  fixed-path failure.
- Git identity uses the authenticated GitHub user’s noreply address,
  eliminating the prior blank-email prompt.
- Git transport uses HTTPS with `gh auth setup-git` as the credential helper; SSH keys and passphrases are not required. The authenticated GitHub CLI token must retain `repo` and `workflow` scopes.
- Post-rebuild manifest regeneration occurs before `pytest`, and the static publisher audit enforces `static viewer -> manifest write -> pytest -> manifest check`: **PASS**.
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

## Release gate

Phase 8 full-text is complete. The final software release depends only on the
nine technical P0 controls, a clean rebuild, tests, CI, manifest, secret scan,
final non-RC metadata and explicit human confirmation. External manuscripts,
journal processes, editorial forms and OSF synchronization are not release
prerequisites.

## rc.5 technical P0 closure

- `B-P0-01` exact dependency lock and Python 3.12 control: **PASS**.
- `B-P0-02` autonomous software/evidence publication gate: **PASS**.
- `B-P0-03` canonical Phase 8 narrative 72/42/13/29/30: **PASS**.
- `B-P0-04` PRISMA-S/structured-search/evidence-traceability metadata: **PASS**.
- `B-P0-05` license/attribution and full-text figure status: **PASS**.
- `B-P0-06` RO-Crate local RIS entity integrity: **PASS**.
- `B-P0-07` CodeMeta/Python runtime consistency: **PASS**.
- `B-P0-08` OSF post-release transaction order and non-blocking behavior: **PASS**.
- `B-P0-09` post-rebuild manifest/checksum regeneration before tests: **PASS**.
- Negative scan for journal-specific names, manuscript paths and article-dependent gate tokens: **PASS**.
- `GO_RELEASE_V2.1.0`: **TRUE for technical eligibility**.
- External GitHub/Zenodo publication: **not executed by this package build**; the BAT requires PR CI and exact human confirmation.
