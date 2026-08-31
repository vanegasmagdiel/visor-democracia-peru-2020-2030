# OSF como complemento del objeto principal preservado en Zenodo

## Política de identidad

El objeto ejecutable y citable principal es el release archivado en Zenodo. OSF
no debe alojar una segunda copia del ZIP como si fuera otro objeto principal.

- DOI conceptual: https://doi.org/10.5281/zenodo.22080540
- DOI v2.0.0: https://doi.org/10.5281/zenodo.22080541
- Repositorio: https://github.com/vanegasmagdiel/visor-democracia-peru-2020-2030

## Disponibilidad operativa verificada

El 2026-08-25, el panel autenticado de la cuenta indicó que no existe un
proyecto OSF y que la creación de nuevos proyectos se encuentra en transición;
la opción de almacenar materiales redirige a repositorios externos, con Zenodo
como recomendación principal. Por ello:

- el automatizador solo sincroniza OSF si se proporciona el GUID de un proyecto
  preexistente y un token `osf.full_write`;
- si no existe ese GUID, OSF se omite sin afectar GitHub, Pages o la validación;
- OSF es opcional y su ausencia o indisponibilidad no bloquea GitHub, Pages,
  Zenodo ni la validación del release.

## Título recomendado del proyecto OSF

**Protocolo y decisiones analíticas del Visor Integrado de Democracia del Perú
2020–2030**

## Descripción

Complemento documental del software de investigación preservado en Zenodo.
Contiene protocolo, decisiones analíticas, matriz de elicitación, trazabilidad de
datos y materiales bibliográficos no ejecutables. El código, el visor y los
releases citables permanecen en GitHub y Zenodo.

## Estructura de componentes

1. `01_Protocolo_y_alcance`
2. `02_Decisiones_analiticas`
3. `03_Elicitacion_de_parametros`
4. `04_Busqueda_bibliografica_fase_8`
5. `05_Materiales_suplementarios`

## Archivos que pueden sincronizarse ahora

- `docs/METODOLOGIA.md`
- `docs/PROVENANCE.md`
- `docs/OSF_COMPLEMENT.md`
- `data/data_status_registry.csv`
- `data/model_config_v2_1.json`
- `data/peru_2025_anchor_summary.csv`
- `data/parameter_elicitation_matrix.csv`
- `data/post_election_evidence_2026.csv`
- `VALIDATION_REPORT.md`
- `docs/FASE_8_PRISMA.md`
- `docs/FASE_8_GATE.md`
- `docs/INFORME_METODOLOGICO_PRISMA_FASE_8_CIERRE_FULLTEXT.md`
- `data/prisma_phase8/phase8_manifest.json`
- `data/prisma_phase8/search_profiles_105.csv`
- `data/prisma_phase8/exclusion_reasons_3.csv`
- `data/prisma_phase8/fulltext_decisions_72.csv`
- `data/prisma_phase8/fulltext_included_29.csv`
- `data/prisma_phase8/fulltext_excluded_13.csv`
- `data/prisma_phase8/fulltext_not_retrieved_30.csv`
- `data/prisma_phase8/evidence_integration_map_29.csv`
- `docs/assets/figura_s1_prisma_fulltext_final.png`

## Archivos que no deben duplicarse

- ZIP completo del release;
- `docs/index.html` autocontenido;
- ejecutables o contenedores;
- copia integral del repositorio;
- informes PDF de terceros;
- archivos EIU protegidos.

## Versionado

- OSF registra el protocolo y las decisiones por fecha.
- Zenodo mantiene el DOI conceptual y los DOI de versión del software.
- Cada registro OSF debe declarar la versión del modelo y el commit GitHub al que
  corresponde.
- Si se registra el protocolo, el registro debe congelarse antes de utilizar sus
  resultados como método ejecutado en el artículo.

## Fase 8

El componente `04_Busqueda_bibliografica_fase_8` puede recibir:

- protocolo de búsqueda;
- bases consultadas;
- strings completos;
- fecha de corte;
- criterios de inclusión y exclusión;
- exportación RIS de los 29 documentos incluidos;
- deduplicación;
- decisiones de los 72 informes buscados;
- corpus final y motivos de exclusión/no recuperación;
- figura PRISMA de elegibilidad cerrada.

Estos materiales documentan el visor y su capa de evidencia. No incluyen
manuscritos ni archivos de postulación.

## Orden transaccional de publicación

- En modo candidato, OSF puede recibir suplementos etiquetados como RC después de CI.
- En modo final, OSF **no se modifica antes de la confirmación humana ni antes del merge/release**.
- El publicador resuelve el SHA final de `main`, crea primero el GitHub Release y solo entonces intenta la sincronización OSF.
- Un fallo de OSF después del GitHub Release se reporta como advertencia y no invalida el release GitHub–Zenodo, porque OSF es opcional.
- El manifiesto OSF final registra el SHA definitivo y el estado `PENDING_ZENODO_INGEST`; cuando Zenodo asigne el DOI de versión, el crosswalk/registro OSF puede actualizarse sin modificar el tag archivado.
