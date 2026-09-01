#!/usr/bin/env python3
from __future__ import annotations
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
PS1 = BASE / "scripts" / "publish_release.ps1"
BAT = BASE / "PUBLICAR_VISOR_V2_1_0.bat"
MANIFEST_SCRIPT = BASE / "scripts" / "build_release_manifest.py"
CI_RESOLVER = BASE / "scripts" / "resolve_ci_run.ps1"
WORKFLOW = BASE / ".github" / "workflows" / "tests.yml"


def strip_literals(text: str) -> str:
    text = re.sub(r'(?ms)@".*?"@', '', text)
    text = re.sub(r"(?ms)@'.*?'@", '', text)
    text = re.sub(r'(?m)#.*$', '', text)
    text = re.sub(r'"(?:`.|[^"`])*"', '""', text)
    text = re.sub(r"'(?:''|[^'])*'", "''", text)
    return text


def balanced(text: str, opening: str, closing: str) -> bool:
    depth = 0
    for char in text:
        if char == opening: depth += 1
        elif char == closing:
            depth -= 1
            if depth < 0: return False
    return depth == 0


def validate() -> list[str]:
    errors: list[str] = []
    ps = PS1.read_text(encoding='utf-8-sig')
    bat = BAT.read_text(encoding='utf-8-sig')
    manifest_script = MANIFEST_SCRIPT.read_text(encoding='utf-8-sig')
    ci_resolver = CI_RESOLVER.read_text(encoding='utf-8-sig')
    workflow = WORKFLOW.read_text(encoding='utf-8-sig')
    cleaned = strip_literals(ps)
    if not balanced(cleaned, '{', '}'): errors.append('PowerShell braces are unbalanced')
    if not balanced(cleaned, '(', ')'): errors.append('PowerShell parentheses are unbalanced')

    required = [
        '[switch]$PublishRelease', '[switch]$DryRun', '[switch]$ValidateFinal',
        'gh" -Arguments @("auth", "setup-git", "--hostname", "github.com")',
        'https://github.com/$Repo.git', 'codex/v2.1.0-rc.5-final-candidate', 'Wait-CandidateCi',
        'scripts\\resolve_ci_run.ps1', 'gh" -Arguments @("run", "watch"', '"run", "view"',
        'Assert-FinalReleaseSlot', 'Assert-PrHeadAndBase',
        'release", "list", "--repo", $Repo, "--limit", "1000", "--json", "tagName"',
        '$Release.PSObject.Properties["tagName"]',
        'CandidateTreeSha', 'FinalTreeSha', 'scripts\\normalize_release_text.py',
        'scripts\\clean_runtime_artifacts.py', 'scripts\\audit_release_hygiene.py',
        'scripts\\build_release_manifest.py', 'PUBLICAR v$Version',
        'release", "create", "v$Version"', '"--draft"',
        'release", "edit", "v$Version", "--repo", $Repo, "--draft=false"', '$script:ReleasePublished = $true',
        'Try-SyncOsfAfterRelease', 'Try-EnsurePagesAfterRelease', 'PENDING_ZENODO_INGEST',
        'Cleanup-CandidateBranchAfterPublished', 'force-with-lease=refs/heads/$CandidateBranch',
        'release", "download"', 'refs/tags/v$Version^{}',
    ]
    for token in required:
        if token not in ps: errors.append(f'PowerShell publisher missing token: {token}')
    prohibited = [
        'git@github.com:', 'Clonando mediante SSH',
        'gh" -Arguments @("pr", "checks"',
        'Where-Object { $_.headSha',
        '"--branch", $CandidateBranch, "--event", "pull_request"',
        '"--delete-branch"',
        '"^\\\\d+$"',
        '-split "\\\\s+"',
        'origin/$CandidateBranch',
        'Sync-OsfSupplements -RepoRoot $CloneRoot -CommitSha $CommitSha',
        'repos/$Repo/releases/tags/v$Version',
        'article_' + 'final_reference_integration_ready', 'SCI' + 'ENDO',
    ]
    for token in prohibited:
        if token.lower() in ps.lower(): errors.append(f'PowerShell publisher contains prohibited token: {token}')
    for token in [
        'No se seleccionan paquetes por comodin',
        'multiples raices validas',
        'El sidecar SHA-256 declara un nombre de archivo distinto',
        'No se pudo confirmar que el slot de GitHub Release este libre',
        'No se pudo verificar acceso al repositorio antes de consultar el slot final',
        'El ZIP descargado del draft release no coincide byte-a-byte',
        'Se reconstruira desde origin/main y se actualizara con force-with-lease',
    ]:
        if token not in ps: errors.append(f'PowerShell publisher missing fail-closed guard: {token}')

    def order(*tokens):
        try: return [ps.index(x) for x in tokens]
        except ValueError: return []
    seq = order('scripts\\build_static_viewer.py', 'scripts\\clean_runtime_artifacts.py',
                'scripts\\normalize_release_text.py', '@("scripts\\build_release_manifest.py")',
                '@("-m", "pytest", "-q", "-p", "no:cacheprovider")',
                '@("scripts\\build_release_manifest.py", "--check")')
    if not seq or seq != sorted(seq): errors.append('deterministic build/normalize/manifest/test order is invalid')
    final_seq = order('Assert-FinalReleaseSlot -RepoRoot $CloneRoot',
                      'Assert-PrHeadAndBase -ExpectedHeadSha $CommitSha -RepoRoot $CloneRoot',
                      'PUBLICAR v$Version', 'gh" -Arguments @("pr", "merge"',
                      '$FinalTreeSha = Invoke-Capture', 'release", "create", "v$Version"',
                      'release", "edit", "v$Version", "--repo", $Repo, "--draft=false"', '$script:ReleasePublished = $true',
                      'Try-SyncOsfAfterRelease -RepoRoot $CloneRoot -CommitSha $FinalCommitSha')
    if not final_seq or final_seq != sorted(final_seq): errors.append('final transaction order is invalid')


    for token in [
        '--commit', 'databaseId,status,conclusion,url,createdAt', 'PSObject.Properties["databaseId"]',
        'GitHub CLI no pudo consultar runs del commit en cuatro intentos consecutivos', 'Sort-Object -Descending',
    ]:
        if token not in ci_resolver:
            errors.append(f'CI resolver missing token: {token}')
    if 'headSha' in ci_resolver or 'Where-Object' in ci_resolver:
        errors.append('CI resolver must rely on gh --commit filtering, not per-object headSha inspection')
    for token in ['Verify exact-run discovery contract', 'Parse PowerShell release scripts', 'scripts/resolve_ci_run.ps1', 'GH_TOKEN: ${{ github.token }}', 'actions: read', 'pull-requests: read', 'github.event.pull_request.head.sha']:
        if token not in workflow:
            errors.append(f'CI workflow missing exact-run discovery guard: {token}')


    manifest_required = [
        'MANIFEST_PATH.write_bytes(manifest_bytes)',
        'CHECKSUM_PATH.write_bytes(checksum_bytes)',
        'actual = path.read_bytes()',
        'expected_output_bytes()',
    ]
    for token in manifest_required:
        if token not in manifest_script:
            errors.append(f'manifest generator missing binary-determinism token: {token}')
    manifest_prohibited = [
        'MANIFEST_PATH.write_text(',
        'CHECKSUM_PATH.write_text(',
        'path.read_text(encoding="utf-8") != expected',
    ]
    for token in manifest_prohibited:
        if token in manifest_script:
            errors.append(f'manifest generator contains platform-sensitive token: {token}')

    for token in ['%~dp0', 'powershell.exe', '%*', 'exit /b %EXIT_CODE%', 'System.Management.Automation.Language.Parser', 'CI_RESOLVER', 'resolve_ci_run.ps1']:
        if token not in bat: errors.append(f'BAT wrapper missing token: {token}')
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print('WINDOWS PUBLISHER STATIC CHECK FAIL')
        for e in errors: print(f'- {e}')
        return 1
    print('WINDOWS PUBLISHER STATIC CHECK OK')
    return 0

if __name__ == '__main__':
    sys.exit(main())
