#!/usr/bin/env python3
"""Static safety audit for the Windows BAT/PowerShell publication entrypoint."""

from __future__ import annotations

import re
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
PS1 = BASE / "scripts" / "publish_release.ps1"
BAT = BASE / "PUBLICAR_VISOR_V2_1_0.bat"


def strip_powershell_literals(text: str) -> str:
    text = re.sub(r"(?ms)^\s*@['\"].*?^['\"]@\s*$", "", text)
    text = re.sub(r"(?m)#.*$", "", text)
    text = re.sub(r"'(?:''|[^'])*'", "''", text)
    text = re.sub(r'"(?:`.|[^"`])*"', '""', text)
    return text


def balanced(text: str, opening: str, closing: str) -> bool:
    depth = 0
    for char in text:
        if char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def validate() -> list[str]:
    errors: list[str] = []
    ps = PS1.read_text(encoding="utf-8-sig")
    bat = BAT.read_text(encoding="utf-8-sig")
    cleaned = strip_powershell_literals(ps)
    if not balanced(cleaned, "{", "}"):
        errors.append("PowerShell braces are unbalanced")
    if not balanced(cleaned, "(", ")"):
        errors.append("PowerShell parentheses are unbalanced")

    required_ps = [
        '[switch]$PublishRelease',
        '[switch]$DryRun',
        '[string]$CandidateRc = "rc.5"',
        '$CandidateLabel = "v$Version-$CandidateRc"',
        'scripts\\validate_phase8.py',
        'fulltext_complete',
        'final_prisma_ready',
        'release_scientific_validation_ready',
        'dependency_lock_ready',
        'release_gate_decoupled',
        'phase8_canonical_narrative',
        'metadata_method_classification',
        'release_doi_status',
        'gh" -Arguments @("release", "create"',
        'No se creo tag, GitHub Release ni DOI',
        'data\\prisma_phase8\\phase8_manifest.json',
        'GitHub writes: NOT ATTEMPTED',
        'fulltext_included_29.csv',
        'requirements-lock.txt',
        'audit_release_independence.py',
        'scripts\\build_release_manifest.py',
        'gh" -Arguments @("pr", "checks"',
        'Try-SyncOsfAfterRelease',
        '$FinalCommitSha = Invoke-Capture',
        'zenodo_current_version_doi_status',
        'gh" -Arguments @("auth", "setup-git", "--hostname", "github.com")',
        '$env:GIT_TERMINAL_PROMPT = "0"',
        'https://github.com/$Repo.git',
        '@("pr", "list", "--repo", $Repo, "--head", $CandidateBranch, "--state", "open", "--json", "url")',
        '$ParsedPrItems = $PrListJson | ConvertFrom-Json',
        '$PrUrl = [string]$PrItems[0].url',
    ]
    for token in required_ps:
        if token not in ps:
            errors.append(f"PowerShell publisher missing token: {token}")
    prohibited = [
        "article_" + "final_reference_integration_ready",
        "SCI" + "ENDO",
        "git@github.com:",
        "Clonando mediante SSH",
    ]
    for token in prohibited:
        if token.lower() in ps.lower():
            errors.append(f"PowerShell publisher contains prohibited token: {token}")
    if '.[0].url // \\"\\"' in ps or '"--state", "all", "--json", "url", "--jq"' in ps:
        errors.append("PowerShell PR lookup contains the legacy jq/backslash quoting pattern")
    if ps.index('if ($PublishRelease)') > ps.index('gh" -Arguments @("release", "create"'):
        errors.append("GitHub release call is not located after the explicit final gate")
    release_create = ps.index('gh" -Arguments @("release", "create"')
    final_sync = ps.index('Try-SyncOsfAfterRelease -RepoRoot $CloneRoot -CommitSha $FinalCommitSha')
    candidate_sync = ps.index('Sync-OsfSupplements -RepoRoot $CloneRoot -CommitSha $CommitSha')
    final_gate = ps.index('if ($PublishRelease) {\n        Write-Step "Comprobando compuerta final"')
    if not (candidate_sync < final_gate < release_create < final_sync):
        errors.append("OSF publication order is not candidate-before-gate / final-after-release")

    static_build = ps.index('scripts\\build_static_viewer.py')
    manifest_write = ps.index('@("scripts\\build_release_manifest.py")')
    pytest_run = ps.index('@("-m", "pytest", "-q")')
    manifest_check = ps.index('@("scripts\\build_release_manifest.py", "--check")')
    if not (static_build < manifest_write < pytest_run < manifest_check):
        errors.append("Release inventory must be regenerated after deterministic rebuild and before pytest")

    https_setup = ps.index('gh" -Arguments @("auth", "setup-git", "--hostname", "github.com")')
    https_clone = ps.index('@("clone", "--filter=blob:none", $HttpsRemote, $CloneRoot)')
    if https_setup > https_clone:
        errors.append("GitHub CLI HTTPS credential helper must be configured before clone")

    required_bat = ["%~dp0", "powershell.exe", "%*", "exit /b %EXIT_CODE%"]
    for token in required_bat:
        if token not in bat:
            errors.append(f"BAT wrapper missing token: {token}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("WINDOWS PUBLISHER STATIC CHECK FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("WINDOWS PUBLISHER STATIC CHECK OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
