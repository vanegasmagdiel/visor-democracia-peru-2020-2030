# Informe metodológico PRISMA — cierre de texto completo

**Proyecto:** Visor Integrado de Democracia del Perú 2020–2030  
**Corte:** 29 de agosto de 2026  
**Versión incorporada:** R4.3.5 / v2.1.0-rc.5

## 1. Función de la búsqueda

El visor es un **producto de investigación original**. La búsqueda estructurada se empleó como método auxiliar para reunir, evaluar y asignar literatura de soporte al marco conceptual, la metodología, la interpretación y las limitaciones. PRISMA 2020 y PRISMA-S aportan trazabilidad al proceso de recuperación y selección; no transforman el diseño principal en una revisión sistemática ni convierten el número de documentos incluidos en un resultado sustantivo del visor.

El diseño principal permanece definido como análisis longitudinal descriptivo de datos secundarios, construcción de un ancla dimensional latente para 2025 y escenarios prospectivos exploratorios con análisis de sensibilidad.

## 2. Recuperación

Se partió de 767 registros. Tras eliminar 116 duplicados y tres registros por otras compuertas, se cribaron 648 títulos/resúmenes; 576 se excluyeron y 72 informes pasaron a recuperación de texto completo.

La recuperación se ejecutó por dos vías legales y verificables:

- 27 documentos de acceso abierto aportados en la carpeta de Google Drive;
- 15 textos completos recuperados de sitios editoriales, SciELO, repositorios institucionales, ONPE, CSIC/JSTOR OA, HydroShare o SSRN.

Los 30 restantes no expusieron texto completo accesible. Cuando solo se localizó resumen, metadatos o una página bajo suscripción, el registro se mantuvo como **no recuperado** y no se simuló una evaluación full-text.

## 3. Cierre PRISMA

| Etapa | n |
|---|---:|
| Registros identificados | 767 |
| Duplicados eliminados | 116 |
| Otras razones de compuerta | 3 |
| Registros cribados | 648 |
| Excluidos por título/resumen | 576 |
| Informes buscados | 72 |
| Informes no recuperados | 30 |
| Informes evaluados a texto completo | 42 |
| Excluidos tras texto completo | 13 |
| Documentos incluidos en el corpus de soporte | 29 |

Comprobaciones: 767 − 116 − 3 = 648; 648 − 576 = 72; 72 − 30 = 42; 42 − 13 = 29.

## 4. Motivos de exclusión a texto completo

| Código | Definición | n |
|---|---|---:|
| `EXC_NO_DIRECT_CONTRIBUTION_TO_ORIGINAL_ARTICLE` | Código histórico: el documento no sostiene una afirmación, dimensión o decisión metodológica del objeto de investigación | 8 |
| `EXC_WRONG_CONSTRUCT_OR_OUTCOME` | Analiza un constructo o desenlace diferente | 2 |
| `EXC_CONTEXT_NOT_TRANSFERABLE` | No ofrece un puente comparativo razonable con el caso peruano | 2 |
| `EXC_OUTSIDE_TEMPORAL_ANALYTIC_SCOPE` | Queda fuera del alcance temporal sin utilidad explicativa actual | 1 |

## 5. Evaluación y reglas de inclusión

La elegibilidad exigió identidad documental confirmada, disponibilidad de texto completo, correspondencia conceptual y una función explícita dentro del objeto de investigación. Se aplicó MMAT 2018 a estudios empíricos, AACODS a tesis/libros/documentos no convencionales y una comprobación de relevancia metodológica a trabajos sobre medición, indicadores compuestos o sensibilidad.

La valoración informó el peso interpretativo, pero no sustituyó la elegibilidad. Ninguna referencia alteró automáticamente los shocks, tasas, correlaciones o bandas del modelo. Cualquier cambio futuro de parámetros requiere una decisión humana fechada y versionada en la matriz de elicitación.

## 6. Integración en el producto de investigación

Los 29 documentos incluidos se asignaron a cinco funciones:

1. definición y medición multidimensional de democracia;
2. contexto de erosión, populismo y desconsolidación latinoamericana;
3. funcionamiento gubernamental, contrapesos, justicia y reforma política;
4. proceso electoral, participación, cultura política y libertades;
5. prospectiva, construcción de indicadores y análisis de sensibilidad.

La matriz `evidence_integration_map_29.csv` registra, para cada fuente, sección destino, rol, dimensión, escenario relacionado, afirmación respaldada, herramienta de appraisal y valoración. El RIS final contiene solo los 29 estudios con texto completo incluido.

## 7. Límites

- La no recuperación de 30 informes puede producir sesgo de disponibilidad.
- La búsqueda no pretende exhaustividad propia de una revisión sistemática sobre democracia peruana.
- El corpus sostiene contexto y decisiones de exposición; no estima efectos causales ni probabilidades de ocurrencia de escenarios.
- Los documentos de terceros no se redistribuyen; se conservan metadatos, trazabilidad y enlaces legítimos.

## 8. Regla de integración

El cierre habilita la regeneración visual y computacional porque están satisfechas las compuertas de recuperación, elegibilidad, trazabilidad y asignación al objeto de investigación. El visor y cualquier producto científico que lo reutilice deben conservar los estados epistemológicos `observado_EIU`, `reportado_secundariamente`, `modelado_latente` y `simulado`, y citar la literatura sin presentar el componente PRISMA como diseño principal.
