# Analytical decision log — canonical scientific and technical release

| Date | Decision | Rationale | Consequence |
|---|---|---|---|
| 2026-08-25 | Keep Peru 2025 total fixed at 5.88 with status `secondary_reported_aggregate`. | The supplied EIU summary lacks a Peru country table; the value is retained through a secondary cross-country replication. | It may be cited only with that qualification. |
| 2026-08-25 | Treat the five Peru 2025 components as latent. | No official 2025 Peru dimensional table was available. | Central values and ensemble must never be called official EIU sub-scores. |
| 2026-08-25 | Build 10,000 zero-sum constrained anchors. | Dimensional uncertainty must propagate while preserving the reported aggregate. | Every sample has exact mean 5.88. |
| 2026-08-25 | Replace evidence weights with categorical priority. | The former numeric field was not a model coefficient and could suggest false precision. | `computational_use=false` for evidence rows. |
| 2026-08-25 | Publish bounded structured judgements for 30 parameters. | Qualitative evidence requires an auditable translation step. | Each parameter has central/low/high, evidence IDs, rule, author and date. |
| 2026-08-25 | Use common random numbers and one residual law. | Scenario comparisons should not be driven by different noise models. | p10–p90 differences primarily reflect scenario assumptions. |
| 2026-08-25 | Label p10–p90 as sensitivity only. | Inputs are not sampling estimates from a probability design. | No confidence-interval or scenario-probability claim is permitted. |
| 2026-08-29 | Close Phase 8 at full text. | Of 72 reports sought, 42 were assessed, 13 excluded, 29 included and 30 not retrieved. | The canonical evidence state is closed; no bibliography row modifies a model parameter automatically. |
| 2026-08-31 | Distribute only the canonical Phase 8 state. | Intermediate screening snapshots can be recovered from Git and should not coexist with current eligibility files in the stable payload. | No pre-full-text archive is shipped in the release. |
| 2026-08-31 | Normalize text payloads to LF and test on Linux and Windows. | Git line-ending normalization previously made a Windows-generated manifest stale in Linux CI. | Rebuild → cleanup → LF normalization → manifest write is the canonical order. |
| 2026-08-31 | Keep Product B autonomous. | A software release must not depend on manuscript status or any journal. | Release gates contain only scientific/software controls; an article may cite the stable DOI later. |
| 2026-08-31 | Keep OSF optional and post-release. | GitHub–Zenodo are the versioned software path. | Candidate mode never writes OSF; final OSF failure cannot invalidate a published GitHub–Zenodo release. |
