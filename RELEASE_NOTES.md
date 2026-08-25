# Release candidate notes — v2.1.0-rc.1 (2026-08-25)

## Status

This is a **scientific review candidate**, not the final Zenodo release. It is
published on a review branch and draft pull request so that the immutable
`v2.0.0` record and DOI remain unchanged while phases 8–11 are pending.

## Scientific corrections completed in phases 1–7

- Separates the secondary-reported Peru 2025 aggregate (`5.88`) from the
  unpublished dimensional composition.
- Replaces the single dimensional calibration with a 10,000-member latent
  anchor ensemble constrained to an exact mean of `5.88`.
- Documents every 2026 shock and structural-rate judgement with central and
  plausible bounds, source identifiers, a translation rule, author and date.
- Removes numeric evidence weights. Evidence priority is categorical and is
  not used as a computational coefficient.
- Propagates anchor, parameter, structural-scale and correlated-residual
  uncertainty through three scenarios using common random numbers.
- Labels p10–p90 as a sensitivity envelope, not a confidence interval and not
  a probability that a scenario will occur.
- Aligns data-status labels across CSV, XLSX, application, static viewer,
  metadata and documentation.

## Reproducibility and dissemination

- Rebuild command: `python scripts/rebuild_scenarios.py`.
- Static GitHub Pages viewer: `python scripts/build_static_viewer.py`.
- Automated preflight, tests, secret scan and deterministic SHA-256 inventory.
- OSF complement limited to protocol, decision log and non-executable review
  materials; the archived software/data object remains in GitHub–Zenodo.

## Publication gate

Do not create tag `v2.1.0`, a GitHub Release or a new Zenodo version until the
phase-8 PRISMA corpus has been incorporated and phases 9–11 have received an
explicit GO. The final release must be built from the accepted main-branch
commit and receive a fresh version DOI under concept DOI
`10.5281/zenodo.22080540`.
