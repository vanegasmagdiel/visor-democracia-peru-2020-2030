# Informe metodológico técnico — PRISMA del Visor de Democracia

## 1. Identificación y estado del corte
- **Proyecto:** `visor_democracia_peru_2020_2030_prisma_fase8`
- **Versión del agente:** `v0.5.6.2-STABLE-CANDIDATE-HF10.4-R4.3.4-CALIBRATION-CONCURRENCY-SAFE-REBASE`
- **Título:** Erosión democrática, medición multidimensional y escenarios prospectivos en el Perú: mapa de evidencia para el periodo 2020–2025 y horizonte 2030
- **Tipo de revisión confirmado:** `scoping_review`.
- **Framework confirmado:** `PCC`.
- **Ventana temporal:** 2000-2026; núcleo analítico 2020-2026; antecedentes clásicos mediante rastreo de citas.
- **Hash metodológico/protocolo:** `b9589694741cd695183523796fea42e8897faa10c8224b562a94dfa63a365f8d`.
- **Estado de reconciliación al corte:** `WARNING_PASS`; `screening_reconciled=false`; pendientes `uncertain=27`.

**Nota de uso en el artículo.** Este documento describe el corte ejecutado hasta screening título/resumen. No anticipa la elegibilidad final ni la inclusión final del estudio, porque la recuperación y evaluación full-text aún están pendientes.

## 2. Pregunta, PCC y alcance
**Pregunta de investigación:** ¿Qué evidencia conceptual, empírica y metodológica permite caracterizar la trayectoria democrática del Perú entre 2020 y 2025 y fundamentar —sin atribución causal— tres escenarios prospectivos auditables hacia 2030, en diálogo con la experiencia latinoamericana y con la evidencia institucional disponible hasta 2026?

### 2.1 Componentes metodológicos registrados
- **Population:** Perú como caso principal; países de América Latina y el Caribe como contexto comparado o fuente de mecanismos y patrones transferibles.
- **Phenomenon:** Erosión democrática, autocratización, régimen híbrido, calidad y medición multidimensional de la democracia, integridad electoral, funcionamiento gubernamental, participación, cultura política, libertades civiles, contrapesos, securitización y prospectiva democrática.
- **Concept:** Erosión democrática, autocratización, régimen híbrido, calidad y medición multidimensional de la democracia, integridad electoral, funcionamiento gubernamental, participación, cultura política, libertades civiles, contrapesos, securitización y prospectiva democrática.
- **Context:** Trayectoria observada 2020-2025, evidencia electoral e institucional disponible en 2026 y horizonte prospectivo 2030. Se admiten antecedentes 2000-2019 para teoría, comparación y construcción metodológica.

## 3. Estrategia de búsqueda
Se ejecutó una estrategia multifuente y multilingüe (español, inglés y portugués), preservando perfiles separados por idioma y módulo. El registro técnico contiene **105 combinaciones perfil × fuente**.

### 3.1 Módulos temáticos
- **Módulo A:** Erosión y calidad democrática.
- **Módulo B:** Dimensiones, instituciones, elecciones y derechos.
- **Módulo C:** Medición democrática, índices, validez e incertidumbre.
- **Módulo D:** Prospectiva, escenarios exploratorios y sensibilidad.
- **Módulo E:** Perú 2026, evidencia electoral e institucional post-electoral.

### 3.2 Fuentes consultadas y rendimiento operativo
Se intentaron consultas en **OpenAlex, Crossref, CORE, arXiv, Scopus, SciELO y Semantic Scholar**. Seis fuentes aportaron registros al corpus; Semantic Scholar produjo cero resultados en este corte.

| Fuente | Perfiles | Registros recuperados (suma por perfil) | Llamadas físicas | Estados de ejecución |
| --- | --- | --- | --- | --- |
| arxiv | 15 | 40 | 2 | OK_WITH_RECORDS=2, SKIPPED_NOT_APPLICABLE=13 |
| core | 15 | 157 | 15 | OK_WITH_RECORDS=14, TIMEOUT_DEFERRED=1 |
| crossref | 15 | 180 | 15 | OK_WITH_RECORDS=15 |
| openalex | 15 | 43 | 15 | OK_WITH_RECORDS=6, OK_ZERO_RESULTS=9 |
| scielo | 15 | 11 | 5 | OK_WITH_RECORDS=2, SKIPPED_CIRCUIT_OPEN=10, SOURCE_BLOCKED=3 |
| scopus | 15 | 336 | 15 | OK_WITH_RECORDS=15 |
| semantic_scholar | 15 | 0 | 10 | OK_ZERO_RESULTS=10, SKIPPED_NOT_APPLICABLE=5 |

### 3.3 Strings completos ejecutados
El siguiente registro se conserva para metodología ampliada/anexo PRISMA-S. Cada fila corresponde al string efectivamente asociado a un perfil, idioma y fuente.

| Perfil | Fuente | Idioma | Rol / módulo | String | Prioridad |
| --- | --- | --- | --- | --- | --- |
| module_A_es | openalex | es | Erosión y calidad democrática | erosión democrática retroceso democrático autocratización régimen híbrido calidad de la democracia Perú América Latina región andina | 1 |
| module_A_es | crossref | es | Erosión y calidad democrática | erosión democrática retroceso democrático autocratización régimen híbrido calidad de la democracia Perú América Latina región andina | 1 |
| module_A_es | semantic_scholar | es | Erosión y calidad democrática | "erosión democrática" "retroceso democrático" autocratización "régimen híbrido" "calidad de la democracia" Perú "América Latina" "región andina" | 1 |
| module_A_es | core | es | Erosión y calidad democrática | erosión democrática retroceso democrático autocratización régimen híbrido calidad de la democracia Perú América Latina región andina | 1 |
| module_A_es | arxiv | es | Erosión y calidad democrática | "erosión democrática" "retroceso democrático" autocratización "régimen híbrido" "calidad de la democracia" Perú "América Latina" "región andina" | 1 |
| module_A_es | scopus | es | Erosión y calidad democrática | ("erosión democrática" OR "retroceso democrático" OR autocratización OR "régimen híbrido" OR "calidad de la democracia") AND (Perú OR "América Latina" OR "región andina") | 1 |
| module_A_es | scielo | es | Erosión y calidad democrática | erosión democrática retroceso democrático autocratización régimen híbrido calidad de la democracia Perú América Latina región andina | 1 |
| module_A_en | openalex | en | Erosión y calidad democrática | democratic erosion democratic backsliding autocratization hybrid regime quality of democracy Peru Latin America Andean region | 1 |
| module_A_en | crossref | en | Erosión y calidad democrática | democratic erosion democratic backsliding autocratization hybrid regime quality of democracy Peru Latin America Andean region | 1 |
| module_A_en | semantic_scholar | en | Erosión y calidad democrática | "democratic erosion" "democratic backsliding" autocratization "hybrid regime" "quality of democracy" Peru "Latin America" "Andean region" | 1 |
| module_A_en | core | en | Erosión y calidad democrática | democratic erosion democratic backsliding autocratization hybrid regime quality of democracy Peru Latin America Andean region | 1 |
| module_A_en | arxiv | en | Erosión y calidad democrática | "democratic erosion" "democratic backsliding" autocratization "hybrid regime" "quality of democracy" Peru "Latin America" "Andean region" | 1 |
| module_A_en | scopus | en | Erosión y calidad democrática | TITLE-ABS-KEY(("democratic erosion" OR "democratic backsliding" OR autocratization OR "hybrid regime" OR "quality of democracy") AND (Peru OR "Latin America" OR "Andean region")) | 1 |
| module_A_en | scielo | en | Erosión y calidad democrática | democratic erosion democratic backsliding autocratization hybrid regime quality of democracy Peru Latin America Andean region | 1 |
| module_A_pt | openalex | pt | Erosión y calidad democrática | erosão democrática retrocesso democrático autocratização regime híbrido qualidade da democracia Peru América Latina região andina | 1 |
| module_A_pt | crossref | pt | Erosión y calidad democrática | erosão democrática retrocesso democrático autocratização regime híbrido qualidade da democracia Peru América Latina região andina | 1 |
| module_A_pt | semantic_scholar | pt | Erosión y calidad democrática | "erosão democrática" "retrocesso democrático" autocratização "regime híbrido" "qualidade da democracia" Peru "América Latina" "região andina" | 1 |
| module_A_pt | core | pt | Erosión y calidad democrática | erosão democrática retrocesso democrático autocratização regime híbrido qualidade da democracia Peru América Latina região andina | 1 |
| module_A_pt | arxiv | pt | Erosión y calidad democrática | "erosão democrática" "retrocesso democrático" autocratização "regime híbrido" "qualidade da democracia" Peru "América Latina" "região andina" | 1 |
| module_A_pt | scopus | pt | Erosión y calidad democrática | ("erosão democrática" OR "retrocesso democrático" OR autocratização OR "regime híbrido" OR "qualidade da democracia") AND (Peru OR "América Latina" OR "região andina") | 1 |
| module_A_pt | scielo | pt | Erosión y calidad democrática | erosão democrática retrocesso democrático autocratização regime híbrido qualidade da democracia Peru América Latina região andina | 1 |
| module_B_es | openalex | es | Dimensiones, instituciones, elecciones y derechos | Perú América Latina región andina integridad electoral funcionamiento del gobierno participación política cultura política libertades civiles controles y contrapesos relaciones Ejecutivo-Congreso securitización | 2 |
| module_B_es | crossref | es | Dimensiones, instituciones, elecciones y derechos | Perú América Latina región andina integridad electoral funcionamiento del gobierno participación política cultura política libertades civiles controles y contrapesos relaciones Ejecutivo-Congreso securitización | 2 |
| module_B_es | semantic_scholar | es | Dimensiones, instituciones, elecciones y derechos | Perú "América Latina" "región andina" "integridad electoral" "funcionamiento del gobierno" "participación política" "cultura política" "libertades civiles" "controles y contrapesos" "relaciones Ejecutivo-Congreso" securitización | 2 |
| module_B_es | core | es | Dimensiones, instituciones, elecciones y derechos | Perú América Latina región andina integridad electoral funcionamiento del gobierno participación política cultura política libertades civiles controles y contrapesos relaciones Ejecutivo-Congreso securitización | 2 |
| module_B_es | arxiv | es | Dimensiones, instituciones, elecciones y derechos | Perú "América Latina" "región andina" "integridad electoral" "funcionamiento del gobierno" "participación política" "cultura política" "libertades civiles" "controles y contrapesos" "relaciones Ejecutivo-Congreso" securitización | 2 |
| module_B_es | scopus | es | Dimensiones, instituciones, elecciones y derechos | (Perú OR "América Latina" OR "región andina") AND ("integridad electoral" OR "funcionamiento del gobierno" OR "participación política" OR "cultura política" OR "libertades civiles" OR "controles y contrapesos" OR "relaciones Ejecutivo-Congreso" OR securitización) | 2 |
| module_B_es | scielo | es | Dimensiones, instituciones, elecciones y derechos | Perú América Latina región andina integridad electoral funcionamiento del gobierno participación política cultura política libertades civiles controles y contrapesos relaciones Ejecutivo-Congreso securitización | 2 |
| module_B_en | openalex | en | Dimensiones, instituciones, elecciones y derechos | Peru Latin America Andean region electoral integrity functioning of government political participation political culture civil liberties checks balances executive-legislative relations securitization | 2 |
| module_B_en | crossref | en | Dimensiones, instituciones, elecciones y derechos | Peru Latin America Andean region electoral integrity functioning of government political participation political culture civil liberties checks balances executive-legislative relations securitization | 2 |
| module_B_en | semantic_scholar | en | Dimensiones, instituciones, elecciones y derechos | Peru "Latin America" "Andean region" "electoral integrity" "functioning of government" "political participation" "political culture" "civil liberties" "checks balances" "executive-legislative relations" securitization | 2 |
| module_B_en | core | en | Dimensiones, instituciones, elecciones y derechos | Peru Latin America Andean region electoral integrity functioning of government political participation political culture civil liberties checks balances executive-legislative relations securitization | 2 |
| module_B_en | arxiv | en | Dimensiones, instituciones, elecciones y derechos | Peru "Latin America" "Andean region" "electoral integrity" "functioning of government" "political participation" "political culture" "civil liberties" "checks balances" "executive-legislative relations" securitization | 2 |
| module_B_en | scopus | en | Dimensiones, instituciones, elecciones y derechos | TITLE-ABS-KEY((Peru OR "Latin America" OR "Andean region") AND ("electoral integrity" OR "functioning of government" OR "political participation" OR "political culture" OR "civil liberties" OR "checks and balances" OR "executive-legislative relations" OR securitization)) | 2 |
| module_B_en | scielo | en | Dimensiones, instituciones, elecciones y derechos | Peru Latin America Andean region electoral integrity functioning of government political participation political culture civil liberties checks balances executive-legislative relations securitization | 2 |
| module_B_pt | openalex | pt | Dimensiones, instituciones, elecciones y derechos | Peru América Latina região andina integridade eleitoral funcionamento do governo participação política cultura política liberdades civis freios e contrapesos relações Executivo-Legislativo securitização | 2 |
| module_B_pt | crossref | pt | Dimensiones, instituciones, elecciones y derechos | Peru América Latina região andina integridade eleitoral funcionamento do governo participação política cultura política liberdades civis freios e contrapesos relações Executivo-Legislativo securitização | 2 |
| module_B_pt | semantic_scholar | pt | Dimensiones, instituciones, elecciones y derechos | Peru "América Latina" "região andina" "integridade eleitoral" "funcionamento do governo" "participação política" "cultura política" "liberdades civis" "freios e contrapesos" "relações Executivo-Legislativo" securitização | 2 |
| module_B_pt | core | pt | Dimensiones, instituciones, elecciones y derechos | Peru América Latina região andina integridade eleitoral funcionamento do governo participação política cultura política liberdades civis freios e contrapesos relações Executivo-Legislativo securitização | 2 |
| module_B_pt | arxiv | pt | Dimensiones, instituciones, elecciones y derechos | Peru "América Latina" "região andina" "integridade eleitoral" "funcionamento do governo" "participação política" "cultura política" "liberdades civis" "freios e contrapesos" "relações Executivo-Legislativo" securitização | 2 |
| module_B_pt | scopus | pt | Dimensiones, instituciones, elecciones y derechos | (Peru OR "América Latina" OR "região andina") AND ("integridade eleitoral" OR "funcionamento do governo" OR "participação política" OR "cultura política" OR "liberdades civis" OR "freios e contrapesos" OR "relações Executivo-Legislativo" OR securitização) | 2 |
| module_B_pt | scielo | pt | Dimensiones, instituciones, elecciones y derechos | Peru América Latina região andina integridade eleitoral funcionamento do governo participação política cultura política liberdades civis freios e contrapesos relações Executivo-Legislativo securitização | 2 |
| module_C_es | openalex | es | Medición democrática, índices, validez e incertidumbre | medición de la democracia índice de democracia índice compuesto dimensión latente validación validez incertidumbre análisis de sensibilidad | 3 |
| module_C_es | crossref | es | Medición democrática, índices, validez e incertidumbre | medición de la democracia índice de democracia índice compuesto dimensión latente validación validez incertidumbre análisis de sensibilidad | 3 |
| module_C_es | semantic_scholar | es | Medición democrática, índices, validez e incertidumbre | "medición de la democracia" "índice de democracia" "índice compuesto" "dimensión latente" validación validez incertidumbre "análisis de sensibilidad" | 3 |
| module_C_es | core | es | Medición democrática, índices, validez e incertidumbre | medición de la democracia índice de democracia índice compuesto dimensión latente validación validez incertidumbre análisis de sensibilidad | 3 |
| module_C_es | arxiv | es | Medición democrática, índices, validez e incertidumbre | "medición de la democracia" "índice de democracia" "índice compuesto" "dimensión latente" validación validez incertidumbre "análisis de sensibilidad" | 3 |
| module_C_es | scopus | es | Medición democrática, índices, validez e incertidumbre | ("medición de la democracia" OR "índice de democracia" OR "índice compuesto" OR "dimensión latente") AND (validación OR validez OR incertidumbre OR "análisis de sensibilidad") | 3 |
| module_C_es | scielo | es | Medición democrática, índices, validez e incertidumbre | medición de la democracia índice de democracia índice compuesto dimensión latente validación validez incertidumbre análisis de sensibilidad | 3 |
| module_C_en | openalex | en | Medición democrática, índices, validez e incertidumbre | democracy measurement democracy index composite index latent dimension validation validity uncertainty sensitivity analysis | 3 |
| module_C_en | crossref | en | Medición democrática, índices, validez e incertidumbre | democracy measurement democracy index composite index latent dimension validation validity uncertainty sensitivity analysis | 3 |
| module_C_en | semantic_scholar | en | Medición democrática, índices, validez e incertidumbre | "democracy measurement" "democracy index" "composite index" "latent dimension" validation validity uncertainty "sensitivity analysis" | 3 |
| module_C_en | core | en | Medición democrática, índices, validez e incertidumbre | democracy measurement democracy index composite index latent dimension validation validity uncertainty sensitivity analysis | 3 |
| module_C_en | arxiv | en | Medición democrática, índices, validez e incertidumbre | "democracy measurement" "democracy index" "composite index" "latent dimension" validation validity uncertainty "sensitivity analysis" | 3 |
| module_C_en | scopus | en | Medición democrática, índices, validez e incertidumbre | TITLE-ABS-KEY(("democracy measurement" OR "democracy index" OR "composite index" OR "latent dimension") AND (validation OR validity OR uncertainty OR "sensitivity analysis")) | 3 |
| module_C_en | scielo | en | Medición democrática, índices, validez e incertidumbre | democracy measurement democracy index composite index latent dimension validation validity uncertainty sensitivity analysis | 3 |
| module_C_pt | openalex | pt | Medición democrática, índices, validez e incertidumbre | mensuração da democracia índice de democracia índice composto dimensão latente validação validade incerteza sensibilidade análise de sensibilidade | 3 |
| module_C_pt | crossref | pt | Medición democrática, índices, validez e incertidumbre | mensuração da democracia índice de democracia índice composto dimensão latente validação validade incerteza sensibilidade análise de sensibilidade | 3 |
| module_C_pt | semantic_scholar | pt | Medición democrática, índices, validez e incertidumbre | "mensuração da democracia" "índice de democracia" "índice composto" "dimensão latente" validação validade incerteza sensibilidade "análise de sensibilidade" | 3 |
| module_C_pt | core | pt | Medición democrática, índices, validez e incertidumbre | mensuração da democracia índice de democracia índice composto dimensão latente validação validade incerteza sensibilidade análise de sensibilidade | 3 |
| module_C_pt | arxiv | pt | Medición democrática, índices, validez e incertidumbre | "mensuração da democracia" "índice de democracia" "índice composto" "dimensão latente" validação validade incerteza sensibilidade "análise de sensibilidade" | 3 |
| module_C_pt | scopus | pt | Medición democrática, índices, validez e incertidumbre | ("mensuração da democracia" OR "índice de democracia" OR "índice composto" OR "dimensão latente") AND (validação OR validade OR incerteza OR sensibilidade OR "análise de sensibilidade") | 3 |
| module_C_pt | scielo | pt | Medición democrática, índices, validez e incertidumbre | mensuração da democracia índice de democracia índice composto dimensão latente validação validade incerteza sensibilidade análise de sensibilidade | 3 |
| module_D_es | openalex | es | Prospectiva, escenarios exploratorios y sensibilidad | prospectiva estudios de futuro planificación por escenarios escenario exploratorio propagación de incertidumbre Monte Carlo análisis de sensibilidad democracia gobernanza institución política | 4 |
| module_D_es | crossref | es | Prospectiva, escenarios exploratorios y sensibilidad | prospectiva estudios de futuro planificación por escenarios escenario exploratorio propagación de incertidumbre Monte Carlo análisis de sensibilidad democracia gobernanza institución política | 4 |
| module_D_es | semantic_scholar | es | Prospectiva, escenarios exploratorios y sensibilidad | prospectiva "estudios de futuro" "planificación por escenarios" "escenario exploratorio" "propagación de incertidumbre" "Monte Carlo" "análisis de sensibilidad" democracia gobernanza "institución política" | 4 |
| module_D_es | core | es | Prospectiva, escenarios exploratorios y sensibilidad | prospectiva estudios de futuro planificación por escenarios escenario exploratorio propagación de incertidumbre Monte Carlo análisis de sensibilidad democracia gobernanza institución política | 4 |
| module_D_es | arxiv | es | Prospectiva, escenarios exploratorios y sensibilidad | prospectiva "estudios de futuro" "planificación por escenarios" "escenario exploratorio" "propagación de incertidumbre" "Monte Carlo" "análisis de sensibilidad" democracia gobernanza "institución política" | 4 |
| module_D_es | scopus | es | Prospectiva, escenarios exploratorios y sensibilidad | (prospectiva OR "estudios de futuro" OR "planificación por escenarios" OR "escenario exploratorio" OR "propagación de incertidumbre" OR "Monte Carlo" OR "análisis de sensibilidad") AND (democracia OR gobernanza OR "institución política") | 4 |
| module_D_es | scielo | es | Prospectiva, escenarios exploratorios y sensibilidad | prospectiva estudios de futuro planificación por escenarios escenario exploratorio propagación de incertidumbre Monte Carlo análisis de sensibilidad democracia gobernanza institución política | 4 |
| module_D_en | openalex | en | Prospectiva, escenarios exploratorios y sensibilidad | foresight future studies scenario planning exploratory scenario uncertainty propagation Monte Carlo sensitivity analysis democracy governance political institution | 4 |
| module_D_en | crossref | en | Prospectiva, escenarios exploratorios y sensibilidad | foresight future studies scenario planning exploratory scenario uncertainty propagation Monte Carlo sensitivity analysis democracy governance political institution | 4 |
| module_D_en | semantic_scholar | en | Prospectiva, escenarios exploratorios y sensibilidad | foresight "future studies" "scenario planning" "exploratory scenario" "uncertainty propagation" "Monte Carlo" "sensitivity analysis" democracy governance "political institution" | 4 |
| module_D_en | core | en | Prospectiva, escenarios exploratorios y sensibilidad | foresight future studies scenario planning exploratory scenario uncertainty propagation Monte Carlo sensitivity analysis democracy governance political institution | 4 |
| module_D_en | arxiv | en | Prospectiva, escenarios exploratorios y sensibilidad | foresight "future studies" "scenario planning" "exploratory scenario" "uncertainty propagation" "Monte Carlo" "sensitivity analysis" democracy governance "political institution" | 4 |
| module_D_en | scopus | en | Prospectiva, escenarios exploratorios y sensibilidad | TITLE-ABS-KEY((foresight OR "future studies" OR "scenario planning" OR "exploratory scenario" OR "uncertainty propagation" OR "Monte Carlo" OR "sensitivity analysis") AND (democracy OR governance OR "political institution")) | 4 |
| module_D_en | scielo | en | Prospectiva, escenarios exploratorios y sensibilidad | foresight future studies scenario planning exploratory scenario uncertainty propagation Monte Carlo sensitivity analysis democracy governance political institution | 4 |
| module_D_pt | openalex | pt | Prospectiva, escenarios exploratorios y sensibilidad | prospectiva estudos de futuro planejamento de cenários cenário exploratório propagação de incerteza Monte Carlo análise de sensibilidade democracia governança instituição política | 4 |
| module_D_pt | crossref | pt | Prospectiva, escenarios exploratorios y sensibilidad | prospectiva estudos de futuro planejamento de cenários cenário exploratório propagação de incerteza Monte Carlo análise de sensibilidade democracia governança instituição política | 4 |
| module_D_pt | semantic_scholar | pt | Prospectiva, escenarios exploratorios y sensibilidad | prospectiva "estudos de futuro" "planejamento de cenários" "cenário exploratório" "propagação de incerteza" "Monte Carlo" "análise de sensibilidade" democracia governança "instituição política" | 4 |
| module_D_pt | core | pt | Prospectiva, escenarios exploratorios y sensibilidad | prospectiva estudos de futuro planejamento de cenários cenário exploratório propagação de incerteza Monte Carlo análise de sensibilidade democracia governança instituição política | 4 |
| module_D_pt | arxiv | pt | Prospectiva, escenarios exploratorios y sensibilidad | prospectiva "estudos de futuro" "planejamento de cenários" "cenário exploratório" "propagação de incerteza" "Monte Carlo" "análise de sensibilidade" democracia governança "instituição política" | 4 |
| module_D_pt | scopus | pt | Prospectiva, escenarios exploratorios y sensibilidad | (prospectiva OR "estudos de futuro" OR "planejamento de cenários" OR "cenário exploratório" OR "propagação de incerteza" OR "Monte Carlo" OR "análise de sensibilidade") AND (democracia OR governança OR "instituição política") | 4 |
| module_D_pt | scielo | pt | Prospectiva, escenarios exploratorios y sensibilidad | prospectiva estudos de futuro planejamento de cenários cenário exploratório propagação de incerteza Monte Carlo análise de sensibilidade democracia governança instituição política | 4 |
| module_E_es | openalex | es | Perú 2026, evidencia electoral e institucional post-electoral | Perú elecciones generales 2026 observación electoral resultados electorales Congreso bicameral seguridad securitización | 5 |
| module_E_es | crossref | es | Perú 2026, evidencia electoral e institucional post-electoral | Perú elecciones generales 2026 observación electoral resultados electorales Congreso bicameral seguridad securitización | 5 |
| module_E_es | semantic_scholar | es | Perú 2026, evidencia electoral e institucional post-electoral | Perú "elecciones generales 2026" "observación electoral" "resultados electorales" "Congreso bicameral" seguridad securitización | 5 |
| module_E_es | core | es | Perú 2026, evidencia electoral e institucional post-electoral | Perú elecciones generales 2026 observación electoral resultados electorales Congreso bicameral seguridad securitización | 5 |
| module_E_es | arxiv | es | Perú 2026, evidencia electoral e institucional post-electoral | Perú "elecciones generales 2026" "observación electoral" "resultados electorales" "Congreso bicameral" seguridad securitización | 5 |
| module_E_es | scopus | es | Perú 2026, evidencia electoral e institucional post-electoral | (Perú) AND ("elecciones generales 2026" OR "observación electoral" OR "resultados electorales" OR "Congreso bicameral" OR seguridad OR securitización) | 5 |
| module_E_es | scielo | es | Perú 2026, evidencia electoral e institucional post-electoral | Perú elecciones generales 2026 observación electoral resultados electorales Congreso bicameral seguridad securitización | 5 |
| module_E_en | openalex | en | Perú 2026, evidencia electoral e institucional post-electoral | Peru general election 2026 election observation electoral results bicameral Congress security securitization | 5 |
| module_E_en | crossref | en | Perú 2026, evidencia electoral e institucional post-electoral | Peru general election 2026 election observation electoral results bicameral Congress security securitization | 5 |
| module_E_en | semantic_scholar | en | Perú 2026, evidencia electoral e institucional post-electoral | Peru "general election 2026" "election observation" "electoral results" "bicameral Congress" security securitization | 5 |
| module_E_en | core | en | Perú 2026, evidencia electoral e institucional post-electoral | Peru general election 2026 election observation electoral results bicameral Congress security securitization | 5 |
| module_E_en | arxiv | en | Perú 2026, evidencia electoral e institucional post-electoral | Peru "general election 2026" "election observation" "electoral results" "bicameral Congress" security securitization | 5 |
| module_E_en | scopus | en | Perú 2026, evidencia electoral e institucional post-electoral | TITLE-ABS-KEY(Peru AND ("general election 2026" OR "election observation" OR "electoral results" OR "bicameral Congress" OR security OR securitization)) | 5 |
| module_E_en | scielo | en | Perú 2026, evidencia electoral e institucional post-electoral | Peru general election 2026 election observation electoral results bicameral Congress security securitization | 5 |
| module_E_pt | openalex | pt | Perú 2026, evidencia electoral e institucional post-electoral | Peru eleições gerais 2026 observação eleitoral resultados eleitorais Congresso bicameral segurança securitização | 5 |
| module_E_pt | crossref | pt | Perú 2026, evidencia electoral e institucional post-electoral | Peru eleições gerais 2026 observação eleitoral resultados eleitorais Congresso bicameral segurança securitização | 5 |
| module_E_pt | semantic_scholar | pt | Perú 2026, evidencia electoral e institucional post-electoral | Peru "eleições gerais 2026" "observação eleitoral" "resultados eleitorais" "Congresso bicameral" segurança securitização | 5 |
| module_E_pt | core | pt | Perú 2026, evidencia electoral e institucional post-electoral | Peru eleições gerais 2026 observação eleitoral resultados eleitorais Congresso bicameral segurança securitização | 5 |
| module_E_pt | arxiv | pt | Perú 2026, evidencia electoral e institucional post-electoral | Peru "eleições gerais 2026" "observação eleitoral" "resultados eleitorais" "Congresso bicameral" segurança securitização | 5 |
| module_E_pt | scopus | pt | Perú 2026, evidencia electoral e institucional post-electoral | (Peru) AND ("eleições gerais 2026" OR "observação eleitoral" OR "resultados eleitorais" OR "Congresso bicameral" OR segurança OR securitização) | 5 |
| module_E_pt | scielo | pt | Perú 2026, evidencia electoral e institucional post-electoral | Peru eleições gerais 2026 observação eleitoral resultados eleitorais Congresso bicameral segurança securitização | 5 |

## 4. Hidratación y normalización de metadatos
- Registros totales en hidratación: **767**.
- Registros elegibles para hidratación: **764**.
- Abstracts antes: **356**.
- Abstracts después: **628**.
- Cobertura de abstracts después de hidratación: **82.2 %**.
- Llamadas API de hidratación: **1072**.
- Batches completados: **35**.

## 5. Deduplicación y corpus maestro
- Registros de entrada: **767**.
- Elegibles tras metadata gate: **764**.
- Duplicados eliminados: **116**.
- Cuarentena: **3**.
- Corpus maestro: **648**.
- Métodos de deduplicación: DOI exacto=57, similitud de título=54, semántica BGE-M3=5.
- Cobertura de abstract del master: **84.72 %** (549/648).

## 6. Screening multimodelo y calibración
- Registros procesados: **648**.
- Contrato válido final: **100.0 %**.
- Primary first-pass válido: **99.85 %**.
- Fallback técnico: **0.0 %**.
- Arquitectura: BGE-M3 (embedding), Qwen3-Embedding 4B (auditor semántico), Qwen3:8B (triage), Qwen3:14B (primary), Qwen3.5:9B (light arbiter), Qwen3.5:27B (deep arbiter), Qwen3.6:27B (false-negative sentinel) y Human Review.
- Los pilotos P10/P50 se emplearon como calibración del procedimiento de screening y no alteran los conteos oficiales PRISMA.

## 7. Resultados PRISMA del corte
| Paso | n | Interpretación |
| --- | --- | --- |
| Registros identificados | 767 | Búsqueda multifuente |
| Duplicados eliminados | 116 | Previo al screening |
| Otras razones / cuarentena | 3 | Metadata gate |
| Registros cribados | 648 | Title/abstract |
| Excluidos title/abstract | 576 | Razones científicas registradas |
| Incluidos provisionales | 45 | Avanzan a recuperación/elegibilidad full-text |
| Inciertos | 27 | No son incluidos finales; requieren resolución |
| Reportes a buscar para recuperación | 72 | 45 incluidos provisionales + 27 inciertos |
| Reportes evaluados para elegibilidad | PENDIENTE | Full-text no ejecutado |
| Estudios incluidos finales | PENDIENTE | No anticipar |

### 7.1 Razones de exclusión
| Código | n | % de excluidos |
| --- | --- | --- |
| EXC_NOT_RELEVANT_CONCEPT | 453 | 78.65 |
| EXC_NOT_GEOGRAPHIC_OR_TRANSFERABLE | 122 | 21.18 |
| EXC_INELIGIBLE_DOCUMENT_TYPE | 1 | 0.17 |

## 8. Human Review y reconciliación
- Registros revisados humanamente: **196**.
- Cambios humano vs IA: **0**.
- No resueltos: **27**.
- Estado: **WARNING_PASS**.
- Por esta razón, el corpus de **45 incluidos provisionales** puede prepararse para recuperación full-text, pero la revisión no debe presentarse todavía como inclusión final cerrada.

## 9. Bibliografía para full-text
Se exporta un RIS con **45 referencias incluidas provisionales**. Los **27 registros uncertain** se excluyen deliberadamente de ese RIS para no mezclar inclusión con incertidumbre; permanecen en la hoja específica del libro Excel.

## 10. Texto técnico condensado para la sección Métodos del artículo
Se realizó una revisión de alcance guiada por PCC y reportada mediante lógica PRISMA 2020/PRISMA-S. La búsqueda fue multifuente y multilingüe, con perfiles diferenciados en español, inglés y portugués y cinco módulos temáticos: (A) erosión y calidad democrática; (B) dimensiones institucionales, electorales y de derechos; (C) medición democrática, índices, validez e incertidumbre; (D) prospectiva, escenarios exploratorios y sensibilidad; y (E) evidencia electoral e institucional peruana de 2026. Se consultaron OpenAlex, Crossref, CORE, arXiv, Scopus, SciELO y Semantic Scholar. Los registros fueron hidratados mediante APIs, normalizados y deduplicados por coincidencia de DOI, similitud de título y verificación semántica. El corpus maestro resultante incluyó 648 registros, sometidos a screening multimodelo de título/resumen con calibración humana. El corte analizado produjo 576 exclusiones, 45 inclusiones provisionales y 27 registros inciertos. La recuperación y evaluación de texto completo permanecen pendientes; por tanto, las inclusiones definitivas de la revisión no se anticipan en este informe.

## 11. Anexo recomendado para el artículo
- Anexo A: tabla íntegra de strings por perfil, idioma y fuente.
- Anexo B: rendimiento por API/fuente y estado de consulta.
- Anexo C: desglose de exclusiones de title/abstract.
- Anexo D: matriz de 45 incluidos provisionales para full-text.
- Anexo E: lista separada de 27 inciertos para resolución posterior.