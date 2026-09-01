# Validation report — v2.1.0

**Validation date:** 2026-08-31  
**Product:** autonomous research software/evidence release.

## Scientific and data controls

- Deterministic model seed `20260825`: **PASS**.
- 10,000 latent 2025 dimensional vectors constrained to mean `5.88`: **PASS**.
- Separation of observed, secondary-reported, latent and simulated states: **PASS**.
- Thirty scenario parameters with documented ranges and evidence translation: **PASS**.
- Three scenario families with bounded p10/p50/p90 sensitivity: **PASS**.
- Phase 8 canonical closure 72/42/13/29/30 and RIS 29: **PASS**.

## Reproducibility and release engineering

- Python runtime policy: 3.12: **PASS**.
- Exact dependency lock: **PASS**.
- Text payload normalization: UTF-8 without BOM, LF: **PASS**.
- Runtime artifact cleanup before inventory: **PASS**.
- Release manifest regenerated after deterministic rebuild and normalization: **PASS**.
- Independent tests, secret scan, independence audit and hygiene audit: **PASS**.
- Linux + Windows GitHub Actions matrix required before final merge.
- CI waits for the workflow run matching the exact candidate head SHA; an absent
  check during GitHub scheduling is polled rather than treated as immediate failure.

## Repository hygiene

- No manuscript or journal-specific release dependency.
- No nested ZIP, sidecar, diagnostic directory, transient cache or attempt-specific
  repair report is part of the release payload.
- Pre-full-text intermediate snapshots are not redistributed in the stable payload;
  history remains available through Git.
- GitHub Pages is not modified by candidate publication.
- OSF is optional and is attempted only after a published GitHub Release.

## Transactional final-release controls

Before merge the publisher verifies:

1. exact PR head SHA and base SHA;
2. successful CI for that exact head SHA;
3. absence of a pre-existing `v2.1.0` tag or GitHub Release;
4. final non-RC metadata and autonomous technical gates;
5. exact human confirmation `PUBLICAR v2.1.0`.

After squash merge it verifies that the final `main` tree is byte-for-byte the
same Git tree as the reviewed candidate. It then runs non-mutating gates,
creates/pushes an annotated tag, builds release assets from that tag, creates a
**draft** GitHub Release, verifies its assets, and only then publishes it. Zenodo
cannot be triggered by an unverified draft. Optional OSF sync occurs after the
published release and is non-blocking.

## Release gate

`GO_RELEASE_V2.1.0` is independent of any article, journal or editorial outcome.
The remaining external gates are successful GitHub CI for the exact candidate
commit and explicit human release confirmation.

## Cross-platform manifest determinism gate

- `RELEASE_MANIFEST.json` and `SHA256SUMS.txt` are generated with raw `write_bytes()` UTF-8/LF output.
- `--check` compares exact `read_bytes()` output, so CRLF/BOM differences cannot be hidden by universal newline translation.
- A second normalization pass after manifest generation provides defense in depth; the two inventory files are excluded from their own hash inventory, avoiding circularity.
- Static and pytest regression checks prohibit reintroduction of platform-sensitive manifest I/O.


## Release-orchestrator hardening

- Exact-head CI watcher: `scripts/resolve_ci_run.ps1` filters GitHub Actions with `--commit <SHA>`; Windows CI executes the same resolver against its current run, and the publisher revalidates the completed run by `headSha`, status, conclusion, and event.
- Package discovery is fail-closed: no wildcard fallback to older ZIPs.
- Source-root discovery rejects ambiguous multi-root archives.
- Candidate branch is preserved through merge and deleted only after the GitHub Release is published and verified.
- Candidate branch is rebuilt from `origin/main` on every attempt and updated with `--force-with-lease`; superseded branch names are not embedded in the release code.
- Draft GitHub Release assets are downloaded and verified by SHA-256 before publication.
- Final release-slot checks distinguish a genuine 404 from authentication/network/API failures.
