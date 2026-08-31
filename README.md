# Visor Integrado de Democracia del Perú 2020–2030 — v2.1.0-rc.5

[![DOI conceptual](https://zenodo.org/badge/DOI/10.5281/zenodo.22080540.svg)](https://doi.org/10.5281/zenodo.22080540)

Aplicación reproducible que integra la trayectoria agregada del *Democracy
Index* 2020–2025 y tres escenarios prospectivos exploratorios para el Perú al
2030. La versión 2.1.0 corrige la trazabilidad del ancla 2025, formaliza los
juicios de escenario y alinea código, documentación y sensibilidad.

**Autor:** Magdiel Torres Vanegas
**ORCID:** https://orcid.org/0000-0002-7913-214X
**Afiliación:** Universidad Nacional de Trujillo, Escuela de Posgrado – Unidad
de Posgrado en Ciencias Económicas; Estudios Axial, Perú
**Perfil:** https://vanegas-magdiel.estudiosaxial.com/
**Repositorio:** https://github.com/vanegasmagdiel/visor-democracia-peru-2020-2030
**Visor web estable:** https://vanegasmagdiel.github.io/visor-democracia-peru-2020-2030/

## Estado de publicación

- DOI conceptual: `10.5281/zenodo.22080540`; DOI estable histórico v2.0.0: `10.5281/zenodo.22080541`.
- Fase 8 cerrada: 767 identificados, 648 cribados, 72 informes buscados, 42 evaluados a texto completo, 13 excluidos y 29 incluidos en el corpus de soporte.
- Las fases 9–11 regeneraron figuras, libro maestro y visor, y ejecutaron el control cruzado del producto computacional.
- El candidato `v2.1.0-rc.5` no crea tag ni DOI automáticamente. La publicación final requiere que las compuertas técnicas estén abiertas, confirmación humana y el modificador explícito `-PublishRelease` del publicador Windows.
- OSF conserva únicamente suplementos metodológicos y no duplica el ZIP principal de Zenodo.
- El visor es autónomo respecto de manuscritos, revistas o decisiones editoriales. Ningún archivo o control de postulación forma parte del release.

## Alcance científico

El producto realiza un **análisis longitudinal descriptivo de datos secundarios
con construcción de escenarios prospectivos exploratorios y análisis de
sensibilidad**.

El proyecto mide calidad democrática mediante las dimensiones del *Democracy
Index*. “Funcionamiento del gobierno” no equivale a una medición directa de
capacidad estatal; esta última solo se emplea como marco interpretativo cuando
corresponde.

## Capas de datos

1. `official_source_observed`: valores publicados en fuentes oficiales.
2. `secondary_reported_aggregate`: agregado 2025 del Perú atribuido al EIU y
   reproducido en una tabla secundaria.
3. `modeled_latent_central`: centro documentado de la composición dimensional
   2025.
4. `modeled_latent_ensemble`: 10 000 composiciones dimensionales admisibles,
   todas con media 5,88.
5. `simulated_scenario`: trayectorias condicionales 2026–2030.

Los cinco valores dimensionales del Perú 2025 **no son subpuntajes oficiales
publicados por EIU**.

## Innovaciones de v2.1.0

- Propaga la incertidumbre de la composición dimensional 2025.
- Publica la matriz completa evidencia–parámetro–rango–regla de traducción.
- Sustituye pesos documentales numéricos no utilizados por prioridades
  categóricas sin uso computacional.
- Muestrea shocks y tasas mediante rangos triangulares explícitos.
- Usa la misma ley residual en los tres escenarios y números aleatorios comunes
  para compararlos.
- Somete la correlación entre dimensiones a sensibilidad 0,00–0,60.
- Elimina los multiplicadores de dispersión por escenario y el factor 0,85 no
  declarado de v2.0.0.
- Separa clasificación de la trayectoria central y envolvente p10–p90.

## Ejecución

### Windows

`run_here.bat`

### PowerShell

`./run_here.ps1`

### Linux/macOS

`bash run_here.sh`

### Reconstrucción científica

```bash
python scripts/rebuild_scenarios.py
python scripts/build_static_viewer.py
python scripts/preflight_check.py
python scripts/build_release_manifest.py --check
pytest -q
```

## Archivos principales

- `app.py`: aplicación Shiny for Python.
- `docs/index.html`: visor estático autocontenido.
- `data/model_config_v2_1.json`: configuración integral.
- `data/peru_2025_anchor_ensemble.csv`: conjunto de anclas latentes.
- `data/peru_2025_anchor_summary.csv`: resumen dimensional.
- `data/parameter_elicitation_matrix.csv`: trazabilidad de 30 parámetros.
- `data/scenario_sensitivity_bands.csv`: envolventes agregadas.
- `data/scenario_sensitivity_by_category.csv`: envolventes dimensionales.
- `docs/METODOLOGIA.md`: especificación metodológica.
- `docs/OSF_COMPLEMENT.md`: política para el complemento OSF.
- `docs/FASE_8_PRISMA.md`: integración, límites y protocolo full-text.
- `docs/FASE_8_GATE.md`: compuerta hacia las fases 9–11.
- `data/prisma_phase8/phase8_manifest.json`: estado canónico y conteos.
- `data/prisma_phase8/fulltext_decisions_72.csv`: decisiones de recuperación y elegibilidad.
- `data/prisma_phase8/fulltext_included_29.csv`: corpus final de soporte.
- `data/prisma_phase8/evidence_integration_map_29.csv`: fuente, afirmación y sección.
- `scripts/validate_phase8.py`: validación cruzada Excel/RIS/CSV/figura.
- `scripts/publish_release.ps1`: publicación transaccional.
- `PUBLICAR_VISOR_V2_1_0.bat`: lanzador Windows.
- `requirements-lock.txt` y `runtime-lock.json`: entorno reproducible fijado.

## Fase 8 y capa de evidencia

La búsqueda bibliográfica estructurada es un método auxiliar de trazabilidad del
producto de investigación. El cierre full-text documenta 72 informes buscados,
42 evaluados, 13 excluidos, 29 documentos incorporados al corpus de soporte y
30 no recuperados. Estos conteos no convierten el diseño principal en una
revisión sistemática ni modifican automáticamente parámetros.

## Interpretación

Los percentiles p10, p50 y p90 son envolventes de sensibilidad. No son
intervalos de confianza, probabilidades de ocurrencia ni pronósticos
electorales. La separación entre escenarios es consecuencia de sus supuestos y
no demuestra dominancia causal.

## Licencias

- Código y configuración original: MIT.
- Documentación y narrativa original: CC BY 4.0.
- Datos derivados: la licencia cubre únicamente la contribución original de
  selección, organización, transformación y modelado.
- Fuentes EIU y otros materiales de terceros conservan sus condiciones y no son
  relicenciados.

Véanse `LICENSE`, `LICENSE_POLICY.md`, `LICENSES/README.md`, `data/LICENSE.md` y
`THIRD_PARTY_NOTICES.md`.

## Cierre científico y técnico

- `data/prisma_phase8/fulltext_decisions_72.csv`: universo full-text auditado.
- `data/prisma_phase8/fulltext_included_29.csv`: corpus final de soporte.
- `data/prisma_phase8/evidence_integration_map_29.csv`: correspondencia fuente–afirmación.
- `docs/assets/figura_s1_prisma_fulltext_final.*`: flujo PRISMA final suplementario.
- `RELEASE_INDEPENDENCE_POLICY.md`: independencia del visor respecto de cualquier producto editorial.
- `RELEASE_GATE_STATUS.json`: estado verificable de las compuertas técnicas.

Ninguna fuente bibliográfica modifica automáticamente los parámetros del modelo.
