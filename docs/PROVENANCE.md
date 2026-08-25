# Provenance and traceability

**Scientific candidate cut-off:** 2026-08-25 (Peru).

## Empirical layers

1. EIU *Democracy Index* editions 2020–2024 provide the observed historical
   series and published dimensional values represented in the package.
2. The Peru 2025 aggregate (`5.88`) is retained as a
   `secondary_reported_aggregate`: it is attributed to the EIU in a supplied
   cross-country secondary table, while the supplied EIU summary does not
   contain a Peru country table.
3. The five Peru 2025 dimensional values are not published EIU sub-scores.
   They form a `modeled_latent_central` vector constrained to average `5.88`.
4. `data/peru_2025_anchor_ensemble.csv` contains 10,000 admissible latent
   compositions, each with exact mean `5.88`. Their distribution represents
   uncertainty in composition, not uncertainty in the fixed aggregate.
5. Values after 2025 are `simulated_scenario` outputs. They are conditional
   analytical trajectories and not event probabilities or forecasts.

## Post-election evidence and analytical judgements

The evidence register is `data/post_election_evidence_2026.csv`. Source
priority is categorical and `computational_use=false`; evidence rows are not
numeric weights. The explicit bridge from sources to each bounded parameter is
published in `data/parameter_elicitation_matrix.csv`, including central
judgement and plausible bounds, source identifiers, translation rule, author,
date and epistemic status.

## Controlled vocabulary

`data/data_status_registry.csv` is authoritative for epistemic-status labels.
The application, static viewer, CSV files, XLSX workbook and documentation must
use those labels consistently.

## Rebuild chain

```text
source tables + calibration audit + model_config_v2_1.json
  -> scripts/rebuild_scenarios.py
  -> anchor ensemble + parameter samples + trajectories + sensitivity bands
  -> scripts/build_static_viewer.py
  -> docs/index.html
  -> preflight + tests + secret scan + SHA-256 manifest
```

The candidate uses deterministic seed `20260825` and 10,000 simulations per
scenario. The p10–p90 outputs are sensitivity envelopes, not confidence
intervals.

## Persistent identifiers

- GitHub repository: https://github.com/vanegasmagdiel/visor-democracia-peru-2020-2030
- Zenodo concept DOI: https://doi.org/10.5281/zenodo.22080540
- Stable v2.0.0 DOI: https://doi.org/10.5281/zenodo.22080541

The `v2.1.0-rc.1` candidate does not mint a DOI. A new version DOI is permitted
only after phases 8–11 and an explicit publication GO.
