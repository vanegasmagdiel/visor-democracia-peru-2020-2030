# Metodología del visor integrado v2.1.0 — versión estable

## 1. Alcance y diseño

El producto realiza un **análisis longitudinal descriptivo de datos secundarios
con construcción de escenarios prospectivos exploratorios y análisis de
sensibilidad**. No estima efectos causales ni probabilidades de ocurrencia de
los escenarios.

El componente empírico mide calidad democrática mediante el *Democracy Index*.
La dimensión *functioning of government* se denomina **funcionamiento del
gobierno** y no se utiliza como sustituto empírico de la capacidad estatal.
Esta última solo puede intervenir como marco interpretativo comparado.

## 2. Estados epistemológicos

El archivo `data/data_status_registry.csv` define los estados utilizados:

1. `official_source_observed`: publicado directamente por una fuente oficial;
2. `secondary_reported_aggregate`: agregado atribuido a la fuente primaria y
   reproducido secundariamente;
3. `modeled_latent_central`: asignación central de una composición no publicada;
4. `modeled_latent_ensemble`: conjunto de composiciones admisibles;
5. `simulated_scenario`: trayectoria condicionada por supuestos explícitos.

El puntaje total del Perú para 2025, 5,88, se registra como
`secondary_reported_aggregate`. Los cinco valores dimensionales del Perú 2025
no fueron publicados en el informe-resumen disponible y no deben citarse como
subpuntajes oficiales del EIU.

## 3. Serie 2020–2025

La capa agregada compara Perú, América Latina y el Caribe y el promedio mundial.
Para 2025 se emplean 5,88 para Perú, 5,71 para América Latina y el Caribe y 5,19
para el mundo. El agregado peruano mejora 0,19 puntos frente a 2024 y permanece
en el intervalo de régimen híbrido.

La comparación dimensional observada del Perú se cierra en 2024. Los valores
dimensionales 2025 se usan únicamente dentro del modelo prospectivo.

## 4. Ancla dimensional latente de 2025

El centro documentado es el vector:

`(8,88; 6,03; 5,07; 3,00; 6,42)`

Su media es exactamente 5,88, pero esta restricción no identifica una única
composición. Por ello, v2.1.0 genera 10 000 vectores admisibles mediante:

1. estimación de volatilidad histórica por dimensión a partir de las diferencias
   anuales 2020–2024;
2. desviación del ancla igual al 50 % de esa volatilidad, con piso 0,08 y techo
   0,40;
3. perturbaciones gaussianas centradas, proyectadas al subespacio de suma cero;
4. truncamiento por límites equivalentes a dos desviaciones alrededor del centro;
5. rechazo de cualquier vector fuera de 0–10;
6. conservación exacta de la media 5,88 en cada simulación.

El conjunto se publica en `peru_2025_anchor_ensemble.csv` y su resumen en
`peru_2025_anchor_summary.csv`.

## 5. Escenarios informados por evidencia

Se mantienen tres escenarios:

1. recuperación institucional y gobernabilidad negociada;
2. continuidad híbrida y estabilización competitiva;
3. deriva restrictiva y securitización.

Los parámetros son **juicios analíticos estructurados y auditables**, no
coeficientes estimados. Cada shock y tasa tiene valor central, rango plausible,
fuentes específicas, señal y regla de traducción en
`parameter_elicitation_matrix.csv`.

El campo `source_priority` del inventario de evidencia es una clasificación
documental. No entra en las ecuaciones y `computational_use` permanece en
`false`. La fecha de corte de evidencia es 17 de agosto de 2026.

## 6. Trayectorias centrales

Para dimensión `i`, escenario `s` y año `t`:

- 2026: `x[i,2026] = clip(x[i,2025] + shock[i,s], 0, 10)`;
- 2027–2030: `x[i,t] = clip(x[i,t-1] + rate[i,s] × decay[t], 0, 10)`;
- `decay = {2027:1,00; 2028:0,90; 2029:0,80; 2030:0,70}`;
- total anual: media aritmética de las cinco dimensiones.

Las trayectorias centrales permiten resumir el escenario, pero no sustituyen la
envolvente de sensibilidad.

## 7. Incertidumbre conjunta

Se simulan 10 000 trayectorias por escenario con semilla `20260825`. El modelo
integra cuatro capas:

1. composición dimensional latente de 2025;
2. shocks y tasas muestreados mediante distribuciones triangulares delimitadas
   por la matriz de elicitación;
3. escala global de las tasas estructurales triangular (0,85; 1,00; 1,15);
4. perturbación residual anual.

La desviación residual es el 25 % de la volatilidad anual observada por
dimensión entre 2020 y 2024, con piso 0,04 y techo 0,20. La correlación común
entre dimensiones se somete a sensibilidad triangular entre 0,00 y 0,60, con
moda 0,30. No se estima una matriz de covarianza debido al número reducido de
observaciones anuales.

Se emplean los mismos números aleatorios entre escenarios para mejorar la
comparabilidad. No se aplican multiplicadores de dispersión específicos por
escenario ni el factor 0,85 de versiones anteriores.

Los percentiles p10, p50 y p90 son **envolventes de sensibilidad**. No son
intervalos de confianza, probabilidades de ocurrencia ni pronósticos electorales.

## 8. Reproducibilidad

El script `scripts/rebuild_scenarios.py` reconstruye:

- anclas latentes;
- trayectorias centrales;
- bandas agregadas y dimensionales;
- resumen de parámetros muestreados;
- resumen 2030.

La configuración completa está en `data/model_config_v2_1.json`. Las pruebas
verifican la media 5,88, los límites 0–10, el número de escenarios, la
reproducibilidad con semilla fija y la concordancia de la matriz de parámetros.

## 9. Limitaciones

- El 5,88 peruano de 2025 se obtuvo mediante reporte secundario y debe sustituirse
  si se obtiene una tabla oficial equivalente.
- La composición dimensional 2025 es latente y dependiente de supuestos.
- Los rangos de shocks y tasas son juicios estructurados de un solo investigador;
  no constituyen una elicitación experta colectiva.
- Cuatro diferencias anuales son insuficientes para estimar robustamente una
  estructura de covarianza.
- La separación entre escenarios es endógena a sus supuestos y no demuestra por
  sí misma que una variable domine causalmente el resultado.
- Eventos posteriores a la fecha de corte pueden invalidar parámetros.

## 10. Capa de evidencia bibliográfica — fase 8

La fase 8 ejecutó una búsqueda bibliográfica estructurada y multilingüe con
trazabilidad PRISMA-S. No constituye el diseño principal ni una revisión de
alcance independiente. Se utilizaron perfiles separados en español, inglés y
portugués, cinco módulos temáticos y siete fuentes: OpenAlex, Crossref, CORE,
arXiv, Scopus, SciELO y Semantic Scholar.

Se identificaron 767 registros. Después del *metadata gate* (3 registros) y la
eliminación de 116 duplicados, se cribaron 648 registros y se excluyeron 576.
Se buscaron 72 informes: 42 fueron recuperados y evaluados a texto completo,
13 se excluyeron, 29 se incorporaron al corpus de soporte y 30 no se
recuperaron. El flujo queda aritméticamente cerrado.

La elegibilidad exigió identidad documental, texto completo verificable,
correspondencia conceptual y función explícita en la capa de evidencia. Se
aplicó MMAT a estudios empíricos, AACODS a literatura no convencional y una
comprobación de relevancia metodológica a trabajos de medición y sensibilidad.

La evidencia bibliográfica no modifica automáticamente los parámetros del
modelo. Cualquier cambio de shock, tasa, correlación o banda requiere una
decisión humana fechada y versionada en la matriz de elicitación. La
especificación completa se conserva en `docs/FASE_8_PRISMA.md`, el cierre en
`docs/INFORME_METODOLOGICO_PRISMA_FASE_8_CIERRE_FULLTEXT.md` y el estado
legible por máquina en `data/prisma_phase8/phase8_manifest.json`.
