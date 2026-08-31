# Release candidate notes — v2.1.0-rc.5 (2026-08-31)

## Status

This is the final technical refactor candidate before `v2.1.0`. It preserves
the immutable `v2.0.0` release and its DOI while the clean candidate is tested
on a branch and draft pull request.

## Scientific corrections

- Separates the secondary-reported Peru 2025 aggregate (`5.88`) from the
  unpublished dimensional composition.
- Propagates a 10,000-member latent-anchor ensemble constrained to an exact
  mean of `5.88`.
- Documents 30 bounded scenario parameters, evidence identifiers and
  translation rules without numeric evidence weights.
- Uses common random numbers, one residual law and seed `20260825`.
- Labels p10–p90 as sensitivity envelopes rather than confidence intervals or
  event probabilities.

## Phase 8 evidence closure

- Records 767 identified and 648 screened records.
- Records 72 reports sought, 42 assessed, 13 excluded, 29 included and 30 not
  retrieved.
- Publishes record-level decisions, appraisal, an evidence-integration map, a
  29-record RIS export and a 300-ppi auxiliary PRISMA figure.
- Treats the literature search as an auxiliary traceability method; it does not
  change model parameters automatically.

## Technical refactor in rc.5

- Pins Python 3.12 and the full dependency graph in
  `requirements-lock.txt`/`runtime-lock.json`.
- Replaces the former article-dependent publication gate with
  `release_scientific_validation_ready`.
- Updates provenance, methodology and decision records to the closed full-text
  state.
- Reclassifies the evidence method as `PRISMA-S`, `structured literature
  search` and `evidence traceability`.
- Removes manuscripts, journal-specific files and editorial submission controls
  from the repository, release archive and OSF synchronization list.
- Adds negative audits that fail if prohibited editorial artifacts or tokens
  enter the release.

## Final release gate

The final `v2.1.0` tag and GitHub Release may be created after the four
technical P0 controls, clean rebuild, tests, CI, manifest, secret scan and human
release confirmation pass. No manuscript submission, journal decision or OSF
synchronization is a precondition.
