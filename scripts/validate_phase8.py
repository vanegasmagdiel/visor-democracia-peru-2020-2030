#!/usr/bin/env python3
"""Validate the completed Phase 8 full-text closure."""
from __future__ import annotations
import csv, json, struct, sys
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]; DATA=BASE/'data/prisma_phase8'; DOCS=BASE/'docs'
def rows(name):
    with (DATA/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def ris(path):return sum(line.startswith('ER  -') for line in path.read_text(encoding='utf-8-sig').splitlines())
def density(path):
    b=path.read_bytes(); off=8
    while off+12<=len(b):
        n=struct.unpack('>I',b[off:off+4])[0]; typ=b[off+4:off+8]; payload=b[off+8:off+8+n]
        if typ==b'pHYs': return struct.unpack('>IIB',payload)
        off+=12+n
def validate():
    errors=[]; s=json.loads((DATA/'phase8_fulltext_summary.json').read_text(encoding='utf-8'))
    expected={'fulltext_decisions_72.csv':72,'fulltext_included_29.csv':29,'fulltext_excluded_13.csv':13,'fulltext_not_retrieved_30.csv':30,'evidence_integration_map_29.csv':29}
    for name,n in expected.items():
        if not (DATA/name).is_file() or len(rows(name))!=n:errors.append(f'{name}: expected {n} rows')
    if not all(s['arithmetic_checks'].values()):errors.append('PRISMA arithmetic failed')
    dec=rows('fulltext_decisions_72.csv'); ids=[x['record_id'] for x in dec]
    if len(ids)!=len(set(ids)):errors.append('duplicate record_id in decisions')
    for state,n in [('included',29),('excluded',13),('not_retrieved',30)]:
        if sum(x['final_inclusion']==state for x in dec)!=n:errors.append(f'{state} count differs')
    if any(not x['parameter_effect'].lower().startswith('none') for x in dec if x['final_inclusion']=='included'):errors.append('automatic parameter effect detected')
    if ris(DATA/'Bibliografia_Incluida_Visor_Democracia_Fulltext_Final_29.ris')!=29:errors.append('final RIS must contain 29 records')
    den=density(DOCS/'assets/figura_s1_prisma_fulltext_final.png')
    if den is None or den[2]!=1 or not(11800<=den[0]<=11820 and 11800<=den[1]<=11820):errors.append('final PRISMA PNG is not 300 ppi')
    gate_text=(DOCS/'FASE_8_GATE.md').read_text(encoding='utf-8')
    if 'PASS — capa de evidencia cerrada' not in gate_text:errors.append('phase 8 evidence gate not closed')
    return {'status':'PASS' if not errors else 'FAIL','release_version':'2.1.0','phase8_state':'fulltext_closed','verified_counts':{'reports_sought':72,'reports_retrieved':42,'reports_assessed':42,'fulltext_excluded':13,'final_included':29,'not_retrieved':30},'ris_records':29,'errors':errors}
def main():
    out=validate(); print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if out['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
