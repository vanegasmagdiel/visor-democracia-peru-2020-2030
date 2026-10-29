import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_approved_public_and_scientific_files_are_frozen():
    provenance=json.loads((ROOT/'PUBLICATION_PROVENANCE.json').read_text(encoding='utf-8'))
    for group in ['public_files_sha256','scientific_files_sha256']:
        for path,digest in provenance[group].items():
            assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path

def test_portal_download_integrity_and_data_correspondence():
    path=ROOT/'scripts/validate_portal.py'
    spec=importlib.util.spec_from_file_location('validate_editorial_portal',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    assert module.run()['result']=='PASS'

def test_approved_header_and_publication_contract():
    page=(ROOT/'docs/index.html').read_text(encoding='utf-8')
    assert 'Edición de revisión · 2.1.1</span>' in page
    assert '.mast>span{flex:0 0 auto;text-align:right;white-space:nowrap}' in page
    assert '<strong>La erosión democrática y el funcionamiento del gobierno en el Perú:' in page
    workflow=(ROOT/'.github/workflows/tests.yml').read_text(encoding='utf-8')
    assert 'needs: test' in workflow
    assert "github.event_name == 'push'" in workflow
    publisher=(ROOT/'scripts/publish_github_release.py').read_text(encoding='utf-8')
    assert "'draft':True" in publisher and "'draft':False" in publisher
    assert 'draft asset failed SHA-256 round trip' in publisher
    assert 'remove_header' in publisher


def test_portal_validator_is_independent_of_windows_default_encoding():
    from unittest.mock import patch
    path=ROOT/'scripts/validate_portal.py'
    spec=importlib.util.spec_from_file_location('portal_with_windows_default',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    original=Path.read_text
    def windows_default(self,*args,**kwargs):
        if not args and kwargs.get('encoding') is None:
            kwargs['encoding']='cp1252'
        return original(self,*args,**kwargs)
    with patch.object(Path,'read_text',windows_default):
        assert module.run()['result']=='PASS'
