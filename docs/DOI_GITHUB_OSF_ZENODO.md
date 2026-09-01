# GitHub, GitHub Pages, Zenodo and OSF — v2.1.0 policy

## Persistent identifiers

- Zenodo concept DOI: https://doi.org/10.5281/zenodo.22080540
- Historical v2.0.0 DOI: https://doi.org/10.5281/zenodo.22080541
- Repository: https://github.com/vanegasmagdiel/visor-democracia-peru-2020-2030
- GitHub Pages: https://vanegasmagdiel.github.io/visor-democracia-peru-2020-2030/

The v2.1.0 version DOI must be accepted only after a verified, published GitHub Release has been ingested by Zenodo. It is never guessed or embedded before minting.

## Candidate mode

Candidate publication is deliberately narrow:

1. verify the ZIP sidecar;
2. rebuild and normalize deterministic outputs;
3. run scientific, independence, hygiene, manifest and secret controls;
4. create/update the candidate branch and draft PR;
5. wait for the exact-head Linux + Windows CI workflow.

Candidate mode does **not** modify `main`, tags, GitHub Releases, GitHub Pages, Zenodo or OSF.

## Final mode

Final mode requires the stable v2.1.0 package and repeats the full candidate validation. Before merge it verifies that the PR head is exactly the CI-tested SHA, that `main` has not moved, and that neither tag nor Release `v2.1.0` exists. After exact human confirmation it squash-merges, verifies candidate/final Git-tree identity, executes non-mutating post-merge checks, pushes an annotated tag, creates a draft Release, verifies both assets, then publishes the Release.

This sequencing prevents an incomplete draft from activating Zenodo. Optional OSF synchronization occurs only after the GitHub Release is published.

## Product independence

No manuscript, journal, editorial form, article DOI or acceptance decision participates in Product B release gates. Scientific articles may later cite the stable version DOI, Git commit and release checksum.
