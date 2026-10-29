#!/usr/bin/env python3
"""Materialize the two approved source archives and verify their exact hashes."""
import argparse
import base64
import hashlib
import io
import json
import subprocess
import urllib.request
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE_COMMIT='4ee5ebfd5120528900c275a5464c01963fe67f3b'
ZENODO_URL='https://zenodo.org/api/records/22223983/files/vanegasmagdiel/visor-democracia-peru-2020-2030-v2.1.0.zip/content'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def rebuild_source():
    meta=json.loads((ROOT/'templates/frozen_v210_zip_metadata.json').read_text(encoding='utf-8'))
    output=io.BytesIO()
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
        archive.comment=base64.b64decode(meta['archive_comment'])
        for item in meta['entries']:
            name=item['filename']
            assert name.startswith('base_cientifica_v210/')
            path=name.removeprefix('base_cientifica_v210/')
            assert path and '..' not in Path(path).parts
            data=subprocess.check_output(['git','show',BASE_COMMIT+':'+path],cwd=ROOT)
            info=zipfile.ZipInfo(name,tuple(item['date_time']))
            for key in ['compress_type','create_system','create_version','extract_version','reserved','flag_bits','volume','internal_attr','external_attr']:
                setattr(info,key,item[key])
            info.extra=base64.b64decode(item['extra'])
            info.comment=base64.b64decode(item['comment'])
            archive.writestr(info,data)
    return output.getvalue()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    manifest=json.loads((ROOT/'docs/manifest.json').read_text(encoding='utf-8'))
    expected={x['path']:x['sha256'] for x in manifest['files'] if x['type']=='ZIP'}
    for relative,checksum in expected.items():
        target=ROOT/'docs'/relative
        if target.name=='base_cientifica_v210.zip':
            # Always reproduce this archive to prove that the source and ZIP metadata agree.
            data=rebuild_source()
        elif target.is_file():
            data=target.read_bytes()
        else:
            assert target.name=='archivo_zenodo_v210.zip'
            with urllib.request.urlopen(ZENODO_URL,timeout=120) as response:
                data=response.read()
        assert digest(data)==checksum,'Archive integrity mismatch: '+relative
        if args.check:
            assert target.is_file() and target.read_bytes()==data,relative
        else:
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(data)
        print('Verified frozen archive:',relative,checksum)

if __name__=='__main__':
    main()
