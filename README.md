# Visor Integrado de Democracia del Perú 2020–2030 — v2.1.0 candidato

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

- DOI conceptual del proyecto: `10.5281/zenodo.22080540`.
- DOI de la versión estable v2.0.0: `10.5281/zenodo.22080541`.
- v2.1.0 permanece como candidato científico mientras se integra la búsqueda
  bibliográfica de la fase 8 y se cierran los productos editoriales de las fases
  9–11.
- No debe crearse una release/DOI v2.1.0 antes de superar esas compuertas.
- La cuenta OSF no contiene un proyecto preexistente y su interfaz ya no permite
  crear proyectos nuevos; el complemento OSF queda condicionado a un GUID
  existente o a la definición posterior de un registro tras la fase 8.

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
- `scripts/publish_release.ps1`: publicación transaccional.
- `PUBLICAR_VISOR_V2_1_0.bat`: lanzador Windows.

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
