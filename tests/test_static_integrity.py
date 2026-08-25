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
    assert 'PUBLICAR v$Version' in publisher
    assert 'release candidate|candidato' in publisher
    assert 'No se creo tag, GitHub Release ni DOI' in publisher


def test_osf_sync_whitelist_excludes_primary_object():
    publisher = (BASE/'scripts/publish_release.ps1').read_text(encoding='utf-8')
    osf_policy = (BASE/'docs/OSF_COMPLEMENT.md').read_text(encoding='utf-8')
    assert 'docs\\METODOLOGIA.md' in publisher
    assert 'data\\parameter_elicitation_matrix.csv' in publisher
    assert 'ZIP completo del release' in osf_policy
    assert 'Sync-OsfFile' in publisher


def test_release_inventory_is_current():
    import importlib.util
    script = BASE/'scripts/build_release_manifest.py'
    spec = importlib.util.spec_from_file_location('release_manifest', script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected_manifest, expected_sums = module.expected_outputs()
    assert (BASE/'RELEASE_MANIFEST.json').read_text(encoding='utf-8') == expected_manifest
    assert (BASE/'SHA256SUMS.txt').read_text(encoding='utf-8') == expected_sums
