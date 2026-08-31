# Integration map: legacy inputs → v2.1.0-rc.5

## Historical layer

- Peru / Latin America and Caribbean / world overall time series.
- Five Democracy Index dimensions through the last published dimensional year.
- Regime classification, score gaps and changes.
- Source, location and epistemic-status fields.

## Scientific correction of the 2025 anchor

- The aggregate `5.88` remains a secondary-reported value.
- The unpublished dimensional composition is no longer treated as observed.
- One central constrained vector and 10,000 latent alternatives are published.
- Every alternative averages exactly `5.88` and remains inside documented
  historical-volatility bounds.

## Prospective layer

- Three scenario families: institutional recovery, hybrid continuity and
  restrictive drift.
- Separate 2026 shock and 2027–2030 structural-rate mechanisms.
- Thirty source-linked parameter judgements with central and plausible values.
- Common-random-number sensitivity with the same residual law in all scenarios.
- Aggregate and dimensional p10–p90 envelopes.

## v2.1.0-rc.1 redesign decisions

- Removed unused numeric evidence weights.
- Removed undocumented scenario-specific dispersion multipliers and the prior
  `0.85` factor.
- Added a controlled data-status registry and field-level dictionary.
- Rebuilt the integral XLSX with audit sheets for anchor, parameters, evidence,
  sensitivity and methodology.
- Aligned the Shiny application, static GitHub Pages viewer, metadata, tests,
  checksums and OSF complement policy.
- Added a transactional Windows publisher whose default mode creates a review
  branch and draft PR but cannot mint the final DOI accidentally.

## v2.1.0-rc.5 Phase 8 layer

```text
PRISMA Excel + 45-record RIS + method report + cut-state PNG
  → immutable source hashes
  → normalized 45/27/72 CSV derivatives
  → validate_phase8.py
  → method-drafting GO / final-release NO-GO
```

This bibliographic layer remains separate from the scenario computation. A
full-text record can affect an article claim or parameter only after human
eligibility, appraisal and an explicit analytical decision.
