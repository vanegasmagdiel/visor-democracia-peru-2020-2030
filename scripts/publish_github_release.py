#!/usr/bin/env python3
"""Publish v2.1.1 from a verified main-branch GitHub Actions run.

Credentials come only from the job-scoped GITHUB_TOKEN environment variable.
The previous release/tag are never changed. A new draft is verified before
publication so the connected Zenodo webhook receives the final release event.
"""
import hashlib
import json
import os
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
VERSION='2.1.1'
TAG='v'+VERSION
REPO='vanegasmagdiel/visor-democracia-peru-2020-2030'

class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        redirected=super().redirect_request(req,fp,code,msg,headers,newurl)
        if redirected is not None and urllib.parse.urlparse(newurl).hostname not in {'api.github.com','uploads.github.com'}:
            redirected.remove_header('Authorization')
        return redirected

def main():
    assert os.environ.get('GITHUB_REPOSITORY')==REPO
    assert os.environ.get('GITHUB_REF')=='refs/heads/main'
    assert os.environ.get('GITHUB_EVENT_NAME')=='push'
    token=os.environ['GITHUB_TOKEN']
    sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    assert sha==os.environ['GITHUB_SHA']
    assert not subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip()
    opener=urllib.request.build_opener(SafeRedirect())

    def request(path,method='GET',payload=None,raw=None,content_type=None,accept='application/vnd.github+json'):
        url=path if path.startswith('https://') else 'https://api.github.com/repos/'+REPO+path
        assert urllib.parse.urlparse(url).hostname in {'api.github.com','uploads.github.com'}
        headers={'Authorization':'Bearer '+token,'Accept':accept,'User-Agent':'visor-release-'+VERSION,'X-GitHub-Api-Version':'2022-11-28'}
        data=raw
        if payload is not None:
            data=json.dumps(payload).encode();headers['Content-Type']='application/json'
        if content_type:headers['Content-Type']=content_type
        with opener.open(urllib.request.Request(url,data=data,headers=headers,method=method),timeout=120) as response:
            result=response.read()
        return result if accept=='application/octet-stream' else json.loads(result)

    for path in ['/releases/tags/'+TAG,'/git/ref/tags/'+TAG]:
        try:
            request(path)
        except urllib.error.HTTPError as exc:
            if exc.code!=404:raise
        else:
            raise RuntimeError('Release slot already exists; refusing to alter '+TAG)
    head=request('/git/ref/heads/main')
    assert head['object']['sha']==sha,'main changed after the validated run'
    output=ROOT/'_exports';output.mkdir(exist_ok=True)
    archive=output/('visor_democracia_peru_2020_2030_'+TAG+'.zip')
    subprocess.run(['git','archive','--format=zip','--prefix=visor_democracia_peru_2020_2030_'+TAG+'/', '-o',str(archive),sha],cwd=ROOT,check=True)
    digest=hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum=output/(archive.name+'.sha256')
    checksum.write_bytes((digest+'  '+archive.name+'\n').encode())
    body=(ROOT/'RELEASE_NOTES.md').read_text(encoding='utf-8')+'\n\n## Source provenance\n\nCommit: `'+sha+'`.\n\nSource archive SHA-256: `'+digest+'`.\n\nThe approved portal package SHA-256 and all frozen scientific/public files are recorded in `PUBLICATION_PROVENANCE.json`.\n'
    release=request('/releases',method='POST',payload={'tag_name':TAG,'target_commitish':sha,'name':'Visor Integrado de Democracia del Perú '+TAG,'body':body,'draft':True,'prerelease':False})
    upload=release['upload_url'].split('{')[0]
    for file in [archive,checksum]:
        asset=request(upload+'?name='+urllib.parse.quote(file.name),method='POST',raw=file.read_bytes(),content_type='application/zip' if file==archive else 'application/octet-stream')
        assert asset['size']==file.stat().st_size
        remote=request(asset['url'],accept='application/octet-stream')
        assert hashlib.sha256(remote).digest()==hashlib.sha256(file.read_bytes()).digest(),'draft asset failed SHA-256 round trip'
    assert request('/git/ref/heads/main')['object']['sha']==sha
    published=request('/releases/'+str(release['id']),method='PATCH',payload={'draft':False,'make_latest':'true'})
    assert published['draft'] is False and published['tag_name']==TAG
    verified=request('/releases/tags/'+TAG)
    assert verified['id']==release['id'] and verified['draft'] is False
    ref=request('/git/ref/tags/'+TAG)['object']
    if ref['type']=='tag':ref=request('/git/tags/'+ref['sha'])['object']
    assert ref['sha']==sha
    print('Published:',verified['html_url'])
    print('Source commit:',sha)
    print('Source SHA-256:',digest)
    print('Zenodo DOI: awaiting the connected repository webhook; no DOI is fabricated.')

if __name__=='__main__':
    main()
