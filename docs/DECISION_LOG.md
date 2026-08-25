# Analytical decision log — phases 1–7

| Date | Decision | Rationale | Consequence |
|---|---|---|---|
| 2026-08-25 | Keep Peru 2025 total fixed at 5.88 with status `secondary_reported_aggregate`. | The supplied EIU summary lacks a Peru country table; the value is retained through a secondary cross-country replication. | It may be cited only with that qualification. |
| 2026-08-25 | Treat the five Peru 2025 components as latent. | No official 2025 Peru dimensional table was available. | Central values and ensemble must never be called official EIU sub-scores. |
| 2026-08-25 | Build 10,000 zero-sum constrained anchors. | Dimensional uncertainty must propagate while preserving the reported aggregate. | Every sample has exact mean 5.88. |
| 2026-08-25 | Replace evidence weights with categorical priority. | The former numeric field was not a model coefficient and could suggest false precision. | `computational_use=false` for evidence rows. |
| 2026-08-25 | Publish bounded structured judgements for 30 parameters. | Qualitative evidence requires an auditable translation step. | Each parameter has central/low/high, evidence IDs, rule, author and date. |
| 2026-08-25 | Use common random numbers and one residual law. | Scenario comparisons should not be driven by different noise models. | p10–p90 differences primarily reflect scenario assumptions. |
| 2026-08-25 | Label p10–p90 as sensitivity only. | Inputs are not sampling estimates from a probability design. | No confidence-interval or scenario-probability claim is permitted. |
| 2026-08-25 | Publish v2.1.0-rc.1 as branch/PR only. | Phase 8 corpus and phases 9–11 remain pending. | No final tag, GitHub Release or new Zenodo DOI before explicit GO. |
