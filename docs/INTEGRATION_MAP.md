# Integration map: legacy viewers → v2.0.0

## Historical viewer contribution

Integrated into the **2020–2025 longitudinal layer**:
- Peru / Latin America / world overall time series.
- Five Democracy Index categories.
- Regime-classification logic.
- Gap and percentage-change calculations.
- Source/provenance fields.

## Prospective viewer contribution

Integrated into the **2026–2030 scenario layer**:
- Category-level scenario mechanics.
- Projection-to-overall aggregation.
- Regime-classification output.
- Prospect-analysis narrative and scenario comparison.

## v2.0.0 redesign decisions

- Two separate applications replaced by one Shiny application with distinct historical and prospective tabs.
- Six legacy prospective variants reduced to three scenario families to improve interpretability and auditability.
- A one-off 2026 post-election shock is separated from 2027–2030 structural rates.
- Projection rates are damped through 2030 instead of using indefinite linear extrapolation.
- Evidence-conditioned coefficients are stored in `data/scenario_coefficients.csv` rather than embedded only in UI logic.
- Monte Carlo p10–p90 envelopes are treated as sensitivity bands, not occurrence probabilities.
- Data status fields distinguish observed EIU values, secondary replication and modeled latent anchors.
- Repository metadata, static viewer, reproducibility script, tests, hashes and DOI-ready metadata were added.
