# Visor Integrado de Democracia del Perú 2020–2030 — v2.0.0

Aplicación reproducible que integra: **(i)** el visor longitudinal 2020–2025 de Perú/América Latina/mundo y **(ii)** un módulo prospectivo 2026–2030 con **tres escenarios** recalibrados después de las elecciones presidenciales peruanas de 2026.

**Autor:** Magdiel Torres Vanegas  
**ORCID:** https://orcid.org/0000-0002-7913-214X  
**Afiliación:** Universidad Nacional de Trujillo, Escuela de Posgrado – Unidad de Posgrado en Ciencias Económicas; Estudios Axial, Perú  
**Perfil:** https://vanegas-magdiel.estudiosaxial.com/  
**Repositorio:** https://github.com/vanegasmagdiel/visor-democracia-peru-2020-2030  
**Visor web:** https://vanegasmagdiel.github.io/visor-democracia-peru-2020-2030/

## Qué cambió en v2.0.0

- Incorpora el **Democracy Index 2025**: Perú 5.88 (régimen híbrido), América Latina y el Caribe 5.71 y mundo 5.19.
- Recalcula brechas, variaciones y comparaciones 2020–2025.
- Integra ambos visores en una sola aplicación Shiny for Python.
- Sustituye los seis escenarios previos por tres escenarios parsimoniosos y auditables: recuperación institucional, continuidad híbrida y deriva restrictiva.
- Condiciona el shock 2026 con evidencia post-electoral (JNE, OEA, UE, Reuters y literatura/analítica especializada).
- Añade bandas de sensibilidad Monte Carlo (p10–p90), explícitamente **no probabilidades de ocurrencia ni intervalos de confianza**.
- Incluye `docs/index.html` autocontenido para GitHub Pages/consulta sin servidor y metadatos para Zenodo/OSF/GitHub.

## Nota crítica de trazabilidad 2025

El informe-resumen EIU 2025 suministrado por el usuario publica los agregados regional y global, pero **no incluye una tabla país con los cinco subpilares del Perú**. Por ello:

- **Perú 2025 = 5.88** se registra como valor observado del EIU, verificado mediante una tabla de serie temporal secundaria que replica el índice.
- Los cinco valores categoriales del Perú 2025 son una **calibración latente del modelo** cuya media es exactamente 5.88. **No deben citarse como subpilares oficiales EIU.**
- Los subpilares 2025 de América Latina y del mundo sí proceden de la Figura 14 del informe EIU 2025.

## Ejecución local

### Windows
`run_here.bat`

### PowerShell
`./run_here.ps1`

### Linux/macOS
`bash run_here.sh`

O manualmente:

```bash
python -m venv .venv
# activar entorno
pip install -r requirements.txt
shiny run --reload app.py
```

## Visor estático

Abrir `docs/index.html`. Está generado con Plotly embebido y no requiere backend.

## Estructura

- `app.py`: visor integrado.
- `data/`: bases auditables CSV + XLSX maestro.
- `docs/index.html`: visor estático autocontenido.
- `docs/METODOLOGIA.md`: modelo y supuestos.
- `docs/PROVENANCE.md`: trazabilidad de fuentes y estatus de datos.
- `CITATION.cff`, `.zenodo.json`, `codemeta.json`: metadatos de citación/DOI.
- `scripts/rebuild_scenarios.py`: reproducción de trayectorias y sensibilidad con semilla fija.
- `scripts/preflight_check.py`: verificación de archivos e invariantes de release.
- `scripts/build_release_manifest.py`: generación y comprobación reproducible del inventario SHA-256.
- `tests/`: validaciones de integridad y modelo.
- `datacite.json`, `ro-crate-metadata.json`: metadatos FAIR/PID complementarios.
- `LICENSE_POLICY.md`: delimitación de licencias para código, documentación, datos derivados y terceros.
- `data/LICENSE.md`: condiciones de reutilización de la capa de datos.

## DOI / publicación

Recomendación: GitHub como repositorio de desarrollo + GitHub Pages desde `/docs` + Zenodo para congelar releases y emitir DOI. OSF puede usarse para registro/preservación adicional. Véase `docs/DOI_GITHUB_OSF_ZENODO.md`. No se incluye un DOI ficticio.

## Licencias

- Código y configuración original: MIT.
- Documentación y narrativa original: CC BY 4.0.
- Datos derivados: CC BY 4.0 únicamente sobre la selección, organización, transformación y contenido original del autor; las fuentes subyacentes conservan sus términos.
- Materiales de terceros: no quedan relicenciados; el PDF de EIU no se redistribuye.

Véanse `LICENSE`, `LICENSE_POLICY.md`, `LICENSES/README.md`, `data/LICENSE.md` y `THIRD_PARTY_NOTICES.md`.

## Integridad de la entrega

`SHA256SUMS.txt` y `RELEASE_MANIFEST.json` se regeneran con `python scripts/build_release_manifest.py`. La comprobación no destructiva se ejecuta con `python scripts/build_release_manifest.py --check`.
