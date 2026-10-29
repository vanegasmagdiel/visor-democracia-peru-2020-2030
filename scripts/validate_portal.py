#!/usr/bin/env python3
"""Offline integrity checks for the portal and its frozen scientific inputs."""
import csv
import hashlib
import json
import re
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'

def run():
    manifest=json.loads((DOCS/'manifest.json').read_text(encoding='utf-8'))
    checked=[]
    for item in manifest['files']:
        p=DOCS/item['path']
        assert p.is_file(),item['path']
        assert p.stat().st_size==item['bytes'],item['path']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],item['path']
        checked.append(item['path'])
    assert len(checked)==len(set(checked))
    source=DOCS/'downloads/base_cientifica_v210.zip'
    with zipfile.ZipFile(source) as z:
        canonical=[]
        for p in (DOCS/'data').rglob('*'):
            if p.is_file():
                assert p.read_bytes()==z.read('base_cientifica_v210/'+p.relative_to(DOCS).as_posix()),str(p)
                canonical.append(p.relative_to(DOCS).as_posix())
    text=(DOCS/'index.html').read_text(encoding='utf-8')
    payload=json.loads(re.search(r'<script id="portal-data" type="application/json">(.*?)</script>',text,re.S)[1])
    for key,path in {'overall':'overall_multilevel_2020_2025.csv','categories':'categories_multilevel_2020_2025.csv','anchor':'peru_2025_anchor_summary.csv','bands':'scenario_sensitivity_bands.csv','bycat':'scenario_sensitivity_by_category.csv','summary':'scenario_summary_2030.csv','parameters':'parameter_elicitation_matrix.csv','evidence':'prisma_phase8/evidence_integration_map_29.csv','fulltext':'prisma_phase8/fulltext_included_29.csv'}.items():
        with (DOCS/'data'/path).open(encoding='utf-8-sig') as f:
            assert payload[key]==list(csv.DictReader(f)),key
    class Links(HTMLParser):
        def __init__(self):super().__init__();self.hrefs=[];self.ids=[]
        def handle_starttag(self,tag,attrs):
            a=dict(attrs)
            if 'href' in a:self.hrefs.append(a['href'])
            if 'id' in a:self.ids.append(a['id'])
    links=[]
    for p in DOCS.glob('*.html'):
        parser=Links();parser.feed(p.read_text(encoding='utf-8'))
        assert len(parser.ids)==len(set(parser.ids)),p.name
        for href in parser.hrefs:
            if re.match(r'^[a-z]+:',href):continue
            if href.startswith('#'):
                assert href[1:] in parser.ids,(p.name,href)
            else:
                assert (p.parent/href.split('#')[0]).is_file(),(p.name,href)
            links.append([p.name,href])
    assert manifest['new_version_doi'] is None
    assert manifest['scientific_version']=='2.1.0'
    assert manifest['scientific_commit']=='4ee5ebfd5120528900c275a5464c01963fe67f3b'
    assert [r['p50'] for r in payload['bands'] if r['year']=='2030']==['6.224','5.874','5.349']
    assert len(payload['evidence'])==29 and len(payload['parameters'])==30
    assert not re.search(r'<script[^>]+src=|<link[^>]+href="https?://',text)
    result={'result':'PASS','download_files_checked':len(checked),'canonical_data_files_equal':len(canonical),'embedded_tables_equal':9,'local_links_checked':len(links),'scientific_doi_unchanged':True,'network_required_for_portal':False}
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    run()
