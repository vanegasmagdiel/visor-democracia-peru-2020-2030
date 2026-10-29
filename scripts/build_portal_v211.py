#!/usr/bin/env python3
"""Build the editorial portal from frozen v2.1.0 files. Standard library only."""
import csv
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
DATA = OUT / 'data'

DESCRIPTIONS = {
 'base_integral_democracia_2020_2030_v2.xlsx':'Base integral de datos y resultados',
 'categories_multilevel_2020_2025.csv':'Serie dimensional: Perú, región y mundo',
 'overall_multilevel_2020_2025.csv':'Serie agregada 2020–2025',
 'data_dictionary.csv':'Diccionario de datos',
 'data_status_registry.csv':'Registro de estados epistemológicos',
 'model_config_v2_1.json':'Configuración del modelo científico',
 'model_formulas_v2.csv':'Fórmulas y transformaciones',
 'parameter_elicitation_matrix.csv':'Matriz de elicitación: shocks, tasas y evidencia',
 'peru_2025_anchor_ensemble.csv':'Ensamble completo: 10 000 anclas latentes',
 'peru_2025_anchor_summary.csv':'Ancla latente: resumen de percentiles',
 'peru_2025_category_calibration_audit.csv':'Auditoría de calibración dimensional 2025',
 'post_election_evidence_2026.csv':'Inventario de evidencia contextual electoral',
 'scenario_coefficients.csv':'Coeficientes centrales de escenarios',
 'scenario_parameter_samples_summary.csv':'Resumen de parámetros muestreados',
 'scenario_sensitivity_bands.csv':'Envolventes agregadas de sensibilidad',
 'scenario_sensitivity_by_category.csv':'Envolventes dimensionales de sensibilidad',
 'scenario_summary_2030.csv':'Resumen de escenarios al 2030',
 'scenario_trajectories_2025_2030.csv':'Trayectorias centrales deterministas',
 'fulltext_included_29.csv':'Corpus incluido: 29 fuentes',
 'fulltext_excluded_13.csv':'Textos completos excluidos: 13 decisiones',
 'fulltext_not_retrieved_30.csv':'Informes no recuperados: 30 registros',
 'fulltext_decisions_72.csv':'Decisiones de los 72 informes buscados',
 'evidence_integration_map_29.csv':'Mapa de integración: fuentes y afirmaciones',
 'search_profiles_105.csv':'Perfiles de búsqueda: 105 consultas',
 'source_performance_7.csv':'Rendimiento de las siete fuentes bibliográficas',
 'phase8_fulltext_summary.json':'Resumen del cierre a texto completo',
 'phase8_manifest.json':'Manifiesto del corpus auxiliar',
 'exclusion_reasons_3.csv':'Catálogo de razones de exclusión',
 'Libro_Analisis_PRISMA_Visor_Democracia_R4_3_5_Cierre_Fulltext.xlsx':'Libro de auditoría bibliográfica PRISMA',
 'Bibliografia_Incluida_Visor_Democracia_Fulltext_Final_29.ris':'Bibliografía incluida en formato RIS',
 'METODOLOGIA.md':'Metodología científica canónica v2.1.0',
 'FASE_8_PRISMA.md':'Protocolo de búsqueda y trazabilidad PRISMA-S',
 'base_cientifica_v210.zip':'Fuente científica completa fijada al commit v2.1.0',
 'archivo_zenodo_v210.zip':'Archivo preservado en Zenodo v2.1.0 (original)',
 'LICENSE_POLICY.md':'Política de licencias por capa',
 'THIRD_PARTY_NOTICES.md':'Reconocimiento de fuentes de terceros',
}

def rows(name):
    with (DATA/name).open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

def page(title, body):
    return '<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><style>body{max-width:820px;margin:40px auto;padding:0 24px;background:#fcfbf8;color:#24221e;font:18px/1.7 Georgia,serif}h1{line-height:1.15}h2{margin-top:35px}a{color:#8b5515;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.7 monospace;background:#f3eee5;padding:20px}p{overflow-wrap:anywhere}.refs p{padding-left:28px;text-indent:-28px}</style><a href="index.html">← Volver al visor</a><h1>'+html.escape(title)+'</h1>'+body+'</html>'

def link_text(s):
    return re.sub(r'https?://[^\s<>]+',lambda m:'<a href="'+m[0]+'">'+m[0]+'</a>',html.escape(s))

def build():
    for name in ['METODOLOGIA.md','FASE_8_PRISMA.md']:
        text=(OUT/name).read_text(encoding='utf-8')
        # A faithful readable plain-text rendering preserves the original method verbatim.
        target='metodologia.html' if name=='METODOLOGIA.md' else 'busqueda_prisma.html'
        (OUT/target).write_text(page(name.replace('.md','').replace('_',' '),'<p>Documento canónico v2.1.0. <a href="'+name+'" download>Descargar original Markdown</a>.</p><pre>'+link_text(text)+'</pre>'),encoding='utf-8')
    references=json.loads((ROOT/'templates/article_references.json').read_text(encoding='utf-8'))
    (OUT/'referencias_articulo.html').write_text(page('Referencias del artículo proporcionado','<p>Transcripción de las referencias del DOCX aprobado adjunto. Se conservan los datos bibliográficos del autor; esta página no certifica una nueva verificación independiente de cada fuente.</p><div class="refs">'+''.join('<p>'+link_text(r)+'</p>' for r in references)+'</div>'),encoding='utf-8')
    files=[]
    for rel in json.loads((ROOT/'templates/portal_download_catalog.json').read_text(encoding='utf-8')):
        p=OUT/rel
        if not p.is_file() or p.name in ['index.html','manifest.json','SHA256SUMS.txt','.nojekyll'] or p.suffix not in ['.csv','.json','.xlsx','.md','.ris','.pdf','.zip']:
            continue
        files.append({'path':p.relative_to(OUT).as_posix(),'description':DESCRIPTIONS.get(p.name,('Figura científica: '+p.stem.replace('_',' ')) if p.suffix=='.pdf' else p.stem.replace('_',' ')), 'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'type':p.suffix[1:].upper()})
    manifest={'portal_version':'2.1.1','status':'candidate_not_published','scientific_version':'2.1.0','scientific_commit':'4ee5ebfd5120528900c275a5464c01963fe67f3b','scientific_doi':'10.5281/zenodo.22223983','new_version_doi':None,'created_local_date':'2026-10-28','files':files}
    selected=[]
    for r in references:
        if r.startswith(('Economist Intelligence Unit.','Magaña,','Page,','Rethlefsen,','Torres Vanegas,')):
            formatted=link_text(r)
            # Apply APA italic title styling where the title is unambiguous.
            if r.startswith('Economist Intelligence Unit.'):
                formatted=re.sub(r'(\(\d{4}\)\. )(.+?)( <a)',r'\1<em>\2</em>\3',formatted)
            if r.startswith('Torres Vanegas,'):
                formatted=formatted.replace('Visor Integrado de Democracia del Perú 2020–2030','<em>Visor Integrado de Democracia del Perú 2020–2030</em>').replace('(Version 2.1.0) [Computer software]','(Versión 2.1.0) [Software]')
            selected.append(formatted)
    payload={'overall':rows('overall_multilevel_2020_2025.csv'),'categories':rows('categories_multilevel_2020_2025.csv'),'anchor':rows('peru_2025_anchor_summary.csv'),'bands':rows('scenario_sensitivity_bands.csv'),'bycat':rows('scenario_sensitivity_by_category.csv'),'summary':rows('scenario_summary_2030.csv'),'parameters':rows('parameter_elicitation_matrix.csv'),'evidence':rows('prisma_phase8/evidence_integration_map_29.csv'),'fulltext':rows('prisma_phase8/fulltext_included_29.csv'),'references':selected,'files':files,'manifest':manifest}
    template=(ROOT/'templates/portal.html').read_text(encoding='utf-8')
    script=(ROOT/'templates/portal.js').read_text(encoding='utf-8')
    result=template.replace('__DATA__',json.dumps(payload,ensure_ascii=False).replace('</','<\\/')).replace('__SCRIPT__',script)
    (OUT/'index.html').write_text(result,encoding='utf-8')
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'SHA256SUMS.txt').write_text(''.join(f['sha256']+'  '+f['path']+'\n' for f in files),encoding='utf-8')
    (OUT/'.nojekyll').touch()
    print(f'Portal built: {len(files)} downloads, {len(result.encode())} HTML bytes')

if __name__=='__main__':
    build()
