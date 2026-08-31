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
    assert 'ZIP completo del release' in osf_policy
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
    assert (BASE/'RELEASE_MANIFEST.json').read_text(encoding='utf-8') == expected_manifest
    assert (BASE/'SHA256SUMS.txt').read_text(encoding='utf-8') == expected_sums


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
