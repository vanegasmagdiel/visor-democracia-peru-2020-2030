# Technical closure report — v2.1.0-rc.5

**Date:** 2026-08-31  
**Scope:** research-software release only

## Decision

`GO_ARTICLE_CORRECTION = TRUE`  
`GO_RELEASE_RC4 = FALSE`  
`GO_RELEASE_RC5_REFACTOR = TRUE`  
`GO_RELEASE_V2.1.0 = TRUE`

The last value expresses technical eligibility after closing the nine P0
controls. It does not mean that an external tag or DOI was created during the
package build.

## P0 evidence

| ID | Closure | Evidence |
|---|---|---|
| B-P0-01 | PASS | Python 3.12 policy, exact top-level requirements, complete `requirements-lock.txt`, runtime lock and BAT installation from the lock |
| B-P0-02 | PASS | `release_scientific_validation_ready` and technical subgates replace the former article-dependent condition |
| B-P0-03 | PASS | active provenance, methodology, decision log and gate use the closed 72/42/13/29/30 state; earlier files are marked historical |
| B-P0-04 | PASS | CFF, CodeMeta and DataCite use PRISMA-S, structured literature search and evidence traceability |
| B-P0-05 | PASS | `LICENSE_POLICY.md` references the 2.1.0 object without invented version DOI and describes the closed full-text PRISMA figure |
| B-P0-06 | PASS | RO-Crate RIS entity points to `Bibliografia_Incluida_Visor_Democracia_Fulltext_Final_29.ris` |
| B-P0-07 | PASS | CodeMeta runtime matches Python `>=3.12,<3.13` and the 3.12 runtime lock |
| B-P0-08 | PASS | candidate OSF sync occurs after CI; final OSF sync occurs only after GitHub Release using final `main` SHA and is non-blocking |
| B-P0-09 | PASS | publisher regenerates manifest/checksums after deterministic rebuild and before pytest; static audit enforces ordering |

## Validation evidence

- scientific rebuild: PASS;
- preflight: PASS;
- Phase 8 validation: PASS;
- test suite: 27/27 PASS;
- release-independence negative audit: PASS;
- secret scan: PASS;
- release manifest: PASS;
- no journal-specific name in the release tree: PASS;
- no manuscript directory or manuscript file: PASS;
- no article-dependent release gate: PASS.

## Publication boundary

The execution BAT pushes a candidate branch, waits for pull-request CI and only
creates tag `v2.1.0` and the GitHub Release after the user enters exactly
`PUBLICAR v2.1.0`. Zenodo may then archive the GitHub Release. OSF is optional and cannot block GitHub–Zenodo. In final mode it is attempted only after the GitHub Release with the final `main` SHA; Zenodo version DOI is synchronized later when available.
