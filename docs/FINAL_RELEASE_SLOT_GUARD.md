# Final release slot guard

The final publication gate checks the release namespace without relying on an expected HTTP 404.

- Git tags are checked independently with `git ls-remote`.
- GitHub Releases are listed with `gh release list --json tagName`.
- An empty release list is a normal successful response.
- API/CLI failure, malformed JSON, or a missing `tagName` field is fail-closed.
- An existing `v2.1.0` tag or GitHub Release blocks merge and publication.

This guard runs before the irreversible human confirmation and before merge/tag/release creation.
