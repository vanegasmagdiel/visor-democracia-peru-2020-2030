# Pre-release integrity patch — v2.1.0-rc.5

Date: 2026-08-31

This patch closes the residual metadata/transaction findings identified by the final Product B audit and the Windows runtime validation:

- B-P0-05: current license/attribution and Phase 8 figure semantics;
- B-P0-06: RO-Crate RIS entity integrity;
- B-P0-07: CodeMeta runtime aligned with Python 3.12 lock;
- B-P0-08: final OSF synchronization moved after GitHub Release, using the final `main` SHA and treated as optional/non-blocking;
- B-P0-09: release manifest and checksum inventory are regenerated after deterministic rebuild outputs and before `pytest`, eliminating the Windows `test_release_inventory_is_current` stale-inventory failure.

No scientific dataset, model coefficient, scenario trajectory or figure content was changed by this patch.
