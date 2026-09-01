import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ORCID = "0000-0002-7913-214X"
REPOSITORY = "https://github.com/vanegasmagdiel/visor-democracia-peru-2020-2030"
REQ = [
    'app.py',
    'README.md',
    'CITATION.cff',
    '.zenodo.json',
    'codemeta.json',
    'datacite.json',
    'ro-crate-metadata.json',
    'LICENSE_POLICY.md',
    'data/LICENSE.md',
    'data/overall_multilevel_2020_2025.csv',
    'data/data_status_registry.csv',
    'data/model_config_v2_1.json',
    'data/peru_2025_anchor_ensemble.csv',
    'data/peru_2025_anchor_summary.csv',
    'data/parameter_elicitation_matrix.csv',
    'data/scenario_sensitivity_by_category.csv',
    'data/base_integral_democracia_2020_2030_v2.xlsx',
    'docs/index.html',
    'docs/.nojekyll',
    'scripts/build_release_manifest.py',
    'scripts/build_data_dictionary.py',
    'scripts/sync_public_data.py',
    'scripts/secret_scan.py',
    'scripts/normalize_release_text.py',
    'scripts/clean_runtime_artifacts.py',
    'scripts/audit_release_hygiene.py',
    'scripts/check_git_clean.py',
    'scripts/publish_release.ps1',
    'PUBLICAR_VISOR_V2_1_0.bat',
    'docs/DECISION_LOG.md',
    'docs/AUDIT_CLOSURE_PHASES_1_7.md',
]


def test_required_files():
    for x in REQ: assert (BASE/x).exists(), x


def test_identity_metadata():
    zenodo = json.loads((BASE/'.zenodo.json').read_text(encoding='utf-8'))
    codemeta = json.loads((BASE/'codemeta.json').read_text(encoding='utf-8'))
    datacite = json.loads((BASE/'datacite.json').read_text(encoding='utf-8'))
    assert zenodo['creators'][0]['orcid'] == ORCID
    assert 'Universidad Nacional de Trujillo' in zenodo['creators'][0]['affiliation']
    assert codemeta['author'][0]['@id'].endswith(ORCID)
    assert codemeta['codeRepository'] == REPOSITORY
    assert datacite['creators'][0]['nameIdentifiers'][0]['nameIdentifier'].endswith(ORCID)
    assert zenodo['version'].startswith('2.1.0')
    assert codemeta['version'].startswith('2.1.0')
    assert datacite['version'].startswith('2.1.0')


def test_evidence_method_metadata_is_correct():
    citation = (BASE/'CITATION.cff').read_text(encoding='utf-8')
    codemeta = json.loads((BASE/'codemeta.json').read_text(encoding='utf-8'))
    datacite = json.loads((BASE/'datacite.json').read_text(encoding='utf-8'))
    combined = citation + json.dumps(codemeta) + json.dumps(datacite)
    assert 'PRISMA-S' in combined
    assert 'structured literature search' in combined
    assert 'PRISMA-ScR' not in combined
    assert 'scoping review' not in combined.lower()


def test_ro_crate_local_parts_exist():
    crate = json.loads((BASE/'ro-crate-metadata.json').read_text(encoding='utf-8'))
    root = next(item for item in crate['@graph'] if item.get('@id') == './')
    for part in root.get('hasPart', []):
        target = part['@id']
        if '://' not in target and not target.startswith('#'):
            assert (BASE/target).exists(), target


def test_layered_license_policy():
    policy = (BASE/'LICENSE_POLICY.md').read_text(encoding='utf-8')
    data_notice = (BASE/'data/LICENSE.md').read_text(encoding='utf-8')
    mit = (BASE/'LICENSE').read_text(encoding='utf-8')
    mit_normalized = ' '.join(mit.split())
    assert 'MIT' in policy and 'CC BY 4.0' in policy
    assert 'fuentes subyacentes conservan sus términos' in policy
    assert 'no distribuye el informe PDF de EIU' in data_notice
    assert 'IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE' in mit_normalized


def test_github_pages_marker():
    assert (BASE/'docs/.nojekyll').is_file()


def test_candidate_publisher_cannot_silently_release():
    publisher = (BASE/'scripts/publish_release.ps1').read_text(encoding='utf-8')
    assert '[switch]$PublishRelease' in publisher
    assert '[switch]$DryRun' in publisher
    assert 'PUBLICAR v$Version' in publisher
    assert 'release candidate|candidato' in publisher
    assert 'No se creo tag, GitHub Release ni DOI' in publisher


def test_osf_sync_whitelist_excludes_primary_object():
    publisher = (BASE/'scripts/publish_release.ps1').read_text(encoding='utf-8')
    osf_policy = (BASE/'docs/OSF_COMPLEMENT.md').read_text(encoding='utf-8')
    assert 'docs\\METODOLOGIA.md' in publisher
    assert 'data\\parameter_elicitation_matrix.csv' in publisher
    assert 'docs\\FASE_8_PRISMA.md' in publisher
    assert 'data\\prisma_phase8\\phase8_manifest.json' in publisher
    assert 'data\\prisma_phase8\\fulltext_decisions_72.csv' in publisher
    assert 'data\\prisma_phase8\\fulltext_included_29.csv' in publisher
    assert 'data\\prisma_phase8\\fulltext_excluded_13.csv' in publisher
    assert 'data\\prisma_phase8\\fulltext_not_retrieved_30.csv' in publisher
    assert 'Bibliografia_Incluida_Visor_Democracia_Fulltext_Final_29.ris' in publisher
    assert 'primary GitHub/Zenodo release ZIP' in osf_policy
    assert 'Sync-OsfFile' in publisher


def test_final_release_requires_autonomous_technical_go():
    publisher = (BASE/'scripts/publish_release.ps1').read_text(encoding='utf-8')
    assert 'fulltext_complete' in publisher
    assert 'final_prisma_ready' in publisher
    assert 'release_scientific_validation_ready' in publisher
    assert 'dependency_lock_ready' in publisher
    assert 'release_gate_decoupled' in publisher
    assert 'phase8_canonical_narrative' in publisher
    assert 'metadata_method_classification' in publisher
    assert 'release_doi_status' in publisher


def test_release_independence_negative_audit():
    import importlib.util
    script = BASE/'scripts/audit_release_independence.py'
    spec = importlib.util.spec_from_file_location('release_independence', script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.audit() == []


def test_dependency_lock_is_exact_and_used_by_publisher():
    lock = (BASE/'requirements-lock.txt').read_text(encoding='utf-8').splitlines()
    assert lock and all('==' in line for line in lock if line.strip() and not line.startswith('#'))
    publisher = (BASE/'scripts/publish_release.ps1').read_text(encoding='utf-8')
    assert 'requirements-lock.txt' in publisher
    assert 'requirements.txt", "pytest"' not in publisher


def test_windows_publisher_static_audit():
    import importlib.util
    script = BASE/'scripts/check_windows_publisher.py'
    spec = importlib.util.spec_from_file_location('check_windows_publisher', script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.validate() == []


def test_release_inventory_is_current():
    import importlib.util
    script = BASE/'scripts/build_release_manifest.py'
    spec = importlib.util.spec_from_file_location('release_manifest', script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected_manifest, expected_sums = module.expected_outputs()
    assert (BASE/'RELEASE_MANIFEST.json').read_bytes() == expected_manifest.encode('utf-8')
    assert (BASE/'SHA256SUMS.txt').read_bytes() == expected_sums.encode('utf-8')


def test_release_manifest_writer_is_binary_and_platform_deterministic():
    script = (BASE/'scripts/build_release_manifest.py').read_text(encoding='utf-8')
    assert 'MANIFEST_PATH.write_bytes(manifest_bytes)' in script
    assert 'CHECKSUM_PATH.write_bytes(checksum_bytes)' in script
    assert 'actual = path.read_bytes()' in script
    assert '.write_text(manifest_text' not in script
    assert '.write_text(checksum_text' not in script
    assert '.read_text(encoding="utf-8") != expected' not in script


def test_ro_crate_all_declared_local_file_entities_exist():
    crate = json.loads((BASE/'ro-crate-metadata.json').read_text(encoding='utf-8'))
    for item in crate['@graph']:
        target = item.get('@id')
        if not isinstance(target, str):
            continue
        if target in {'./', 'ro-crate-metadata.json'} or '://' in target or target.startswith('#'):
            continue
        if item.get('@type') == 'File' or (isinstance(item.get('@type'), list) and 'File' in item.get('@type')):
            assert (BASE/target).exists(), target


def test_codemeta_runtime_matches_canonical_python_policy():
    codemeta = json.loads((BASE/'codemeta.json').read_text(encoding='utf-8'))
    runtime = json.loads((BASE/'runtime-lock.json').read_text(encoding='utf-8'))
    pyproject = (BASE/'pyproject.toml').read_text(encoding='utf-8')
    assert codemeta['runtimePlatform'] == 'Python >=3.12,<3.13'
    assert runtime['python'] == '3.12'
    assert 'requires-python = ">=3.12,<3.13"' in pyproject


def test_license_policy_has_closed_phase8_and_no_editorial_release_dependency():
    policy = (BASE/'LICENSE_POLICY.md').read_text(encoding='utf-8')
    assert 'Figura PRISMA del cierre full-text' in policy
    assert 'no representa el flujo full-text final' not in policy
    assert 'hasta completar las fases bibliográfica y editorial' not in policy


def test_osf_final_sync_is_post_release_and_non_blocking():
    publisher = (BASE/'scripts/publish_release.ps1').read_text(encoding='utf-8')
    assert 'Try-SyncOsfAfterRelease' in publisher
    assert 'PENDING_ZENODO_INGEST' in publisher
    assert publisher.index('gh" -Arguments @("release", "create"') < publisher.index('Try-SyncOsfAfterRelease -RepoRoot $CloneRoot -CommitSha $FinalCommitSha')
    assert 'OSF es opcional y puede sincronizarse despues' in publisher



def test_release_hygiene_audit():
    import importlib.util
    script = BASE/'scripts/audit_release_hygiene.py'
    spec = importlib.util.spec_from_file_location('release_hygiene', script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.audit() == []


def test_text_payloads_are_lf_and_without_bom():
    import importlib.util
    script = BASE/'scripts/normalize_release_text.py'
    spec = importlib.util.spec_from_file_location('normalize_release_text', script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for path in module.candidates():
        raw = path.read_bytes()
        assert not raw.startswith(b'\xef\xbb\xbf'), path
        assert b'\r\n' not in raw and b'\r' not in raw, path


def test_ci_is_cross_platform_and_manifest_precedes_pytest():
    workflow = (BASE/'.github/workflows/tests.yml').read_text(encoding='utf-8')
    assert 'ubuntu-24.04' in workflow and 'windows-2025' in workflow
    assert 'actions/checkout@v7.0.1' in workflow
    assert 'actions/setup-python@v7.0.0' in workflow
    assert 'actions: read' in workflow and 'pull-requests: read' in workflow
    assert 'Verify exact-run discovery contract' in workflow
    assert 'Parse PowerShell release scripts' in workflow
    assert 'scripts/resolve_ci_run.ps1' in workflow
    assert 'github.event.pull_request.head.sha' in workflow
    assert "github.event_name == 'pull_request'" in workflow
    assert 'normalize_release_text.py' in workflow
    assert 'audit_release_hygiene.py' in workflow
    assert workflow.index('python scripts/build_release_manifest.py\n') < workflow.index('pytest -q')
    assert 'on: [push, pull_request]' not in workflow


def test_release_gate_contains_only_product_b_state():
    gate = json.loads((BASE/'RELEASE_GATE_STATUS.json').read_text(encoding='utf-8'))
    serialized = json.dumps(gate).lower()
    assert 'go_article' not in serialized
    assert 'go_release_rc4' not in serialized
    assert gate['product'] == 'research_software_and_evidence'
    assert 'journal_submission' in gate['release_gate_forbids']


def test_publisher_waits_for_exact_head_ci_and_uses_draft_release():
    publisher = (BASE/'scripts/publish_release.ps1').read_text(encoding='utf-8')
    assert 'Wait-CandidateCi' in publisher
    resolver = (BASE/'scripts/resolve_ci_run.ps1').read_text(encoding='utf-8')
    assert 'scripts\\resolve_ci_run.ps1' in publisher
    assert '--commit' in resolver
    assert 'PSObject.Properties["databaseId"]' in resolver
    assert 'Sort-Object -Descending' in resolver
    assert 'headSha' not in resolver
    assert 'Where-Object' not in resolver
    assert 'gh" -Arguments @("run", "watch"' in publisher
    assert 'gh" -Arguments @(' in publisher and '"run", "view", $RunId' in publisher
    assert '$Result.PSObject.Properties["headSha"]' in publisher
    assert 'Assert-FinalReleaseSlot' in publisher
    assert 'Assert-PrHeadAndBase' in publisher
    assert '"release", "list", "--repo", $Repo, "--limit", "1000", "--json", "tagName"' in publisher
    assert '$Release.PSObject.Properties["tagName"]' in publisher
    assert 'repos/$Repo/releases/tags/v$Version' not in publisher
    assert '--draft' in publisher
    assert 'release", "download"' in publisher
    assert 'El ZIP descargado del draft release no coincide byte-a-byte' in publisher
    assert 'release", "edit", "v$Version", "--repo", $Repo, "--draft=false"' in publisher
    assert 'CandidateTreeSha' in publisher and 'FinalTreeSha' in publisher
    assert publisher.index('Assert-FinalReleaseSlot -RepoRoot $CloneRoot') < publisher.index('gh" -Arguments @("pr", "merge"')


def test_publisher_is_fail_closed_and_preserves_recovery_branch_until_release():
    publisher = (BASE/'scripts/publish_release.ps1').read_text(encoding='utf-8')
    assert 'No se seleccionan paquetes por comodin' in publisher
    assert 'multiples raices validas' in publisher
    assert 'El sidecar SHA-256 declara un nombre de archivo distinto' in publisher
    assert 'No se pudo confirmar que el slot de GitHub Release este libre' in publisher
    assert 'No se pudo verificar acceso al repositorio antes de consultar el slot final' in publisher
    assert '"--delete-branch"' not in publisher
    assert 'Cleanup-CandidateBranchAfterPublished' in publisher
    assert '"^\\d+$"' in publisher
    assert '-split "\\s+"' in publisher
    assert '"^\\\\d+$"' not in publisher
    assert '-split "\\\\s+"' not in publisher
    assert 'force-with-lease=refs/heads/$CandidateBranch' in publisher
    assert 'origin/$CandidateBranch' not in publisher
    published = publisher.index('$script:ReleasePublished = $true')
    cleanup_candidate = publisher.index('Cleanup-CandidateBranchAfterPublished -RepoRoot $CloneRoot')
    assert published < cleanup_candidate


def test_windows_wrapper_parses_publisher_before_execution():
    bat = (BASE/'PUBLICAR_VISOR_V2_1_0.bat').read_text(encoding='utf-8')
    assert 'System.Management.Automation.Language.Parser' in bat
    assert 'CI_RESOLVER' in bat and 'resolve_ci_run.ps1' in bat
    assert bat.index('System.Management.Automation.Language.Parser') < bat.index('-File "%PS_SCRIPT%"')


def test_candidate_mode_has_no_pages_or_osf_side_effects():
    publisher = (BASE/'scripts/publish_release.ps1').read_text(encoding='utf-8')
    assert '[OMITIDO] OSF y GitHub Pages no se modifican en modo candidato.' in publisher
    assert 'Sync-OsfSupplements -RepoRoot $CloneRoot -CommitSha $CommitSha' not in publisher
    assert 'Try-EnsurePagesAfterRelease' in publisher


def test_final_release_marks_published_before_post_publish_verification():
    publisher = (BASE/'scripts/publish_release.ps1').read_text(encoding='utf-8')
    edit = publisher.index('release", "edit", "v$Version", "--repo", $Repo, "--draft=false"')
    marked = publisher.index('$script:ReleasePublished = $true', edit)
    verify = publisher.index('$PublishedJson = Invoke-Capture', edit)
    assert edit < marked < verify
