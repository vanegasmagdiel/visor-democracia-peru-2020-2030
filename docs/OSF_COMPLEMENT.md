# OSF as an optional complement to the GitHub–Zenodo software object

## Identity policy

The executable/citable software object is the stable GitHub Release preserved in Zenodo. OSF must not host a duplicate primary ZIP.

- Concept DOI: https://doi.org/10.5281/zenodo.22080540
- Historical v2.0.0 DOI: https://doi.org/10.5281/zenodo.22080541
- Repository: https://github.com/vanegasmagdiel/visor-democracia-peru-2020-2030

## Transaction policy

- Candidate mode never writes to OSF.
- Final mode never writes to OSF before human confirmation, merge, tag and publication of the verified GitHub Release.
- OSF is attempted only when a pre-existing project GUID and write token are deliberately supplied.
- OSF failure is non-blocking after the GitHub Release because OSF is supplementary.
- The final OSF manifest records the final `main` SHA and `PENDING_ZENODO_INGEST`; after Zenodo mints the v2.1.0 DOI, the crosswalk/OSF record may be updated without modifying the frozen Git tag/release.

## Eligible supplementary materials

- methodology and provenance documentation;
- analytical decision log;
- data-status registry and model configuration;
- parameter-elicitation matrix;
- post-election evidence register;
- Phase 8 protocol, canonical manifest, full-text decisions and final 29-record RIS;
- final auxiliary PRISMA figure;
- validation report and release-independence policy.

## Excluded materials

- primary GitHub/Zenodo release ZIP;
- self-contained executable viewer as a duplicate primary object;
- repository clone or containers;
- third-party PDFs or protected EIU reports;
- manuscript/journal submission files;
- pre-full-text intermediate snapshots;
- diagnostic logs, caches or attempt-specific repair reports.
