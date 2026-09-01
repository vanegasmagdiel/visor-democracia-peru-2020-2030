# Independence policy for the research-software release

The Visor Integrado de Democracia del Perú 2020–2030 is an autonomous research
software product. Its publication, preservation and versioning are governed by
the integrity of its code, derived data, model, evidence layer, tests,
provenance, licenses and persistent identifiers.

## Allowed release dependencies

- clean scientific rebuild;
- model and data validation;
- Phase 8 evidence-layer closure;
- exact dependency lock;
- test and CI success;
- release manifest and SHA-256 verification;
- secret scan;
- final non-RC metadata;
- explicit human release confirmation.

## Prohibited release dependencies

- manuscript readiness;
- journal template or submission status;
- sworn declarations or editorial forms;
- peer-review or acceptance decisions;
- an article DOI;
- OSF availability or synchronization.

External scientific outputs may cite a stable visor version through its Zenodo
version DOI, Git commit and package SHA-256. Those references create
traceability, not a transactional dependency. OSF remains an optional
methodological complement and never duplicates or blocks the GitHub–Zenodo
software object.
