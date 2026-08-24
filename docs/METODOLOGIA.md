# Metodología del visor integrado v2.0.0

## 1. Arquitectura analítica

El visor separa estrictamente **observación**, **calibración** y **escenario**. La capa longitudinal 2020–2025 contiene datos observados, salvo el vector categorial Perú-2025, que es un estado latente calibrado. La capa 2026–2030 es prospectiva y no pretende estimar probabilidades electorales.

## 2. Actualización 2025

El puntaje peruano pasa de 5.69 (2024) a 5.88 (2025): +0.19 puntos. América Latina y el Caribe pasa de 5.61 a 5.71 y el promedio mundial de 5.17 a 5.19. El Perú continúa en régimen híbrido.

La Figura 14 del EIU 2025 reporta para América Latina: proceso electoral 7.14; funcionamiento del gobierno 5.13; participación 5.69; cultura política 4.30; libertades civiles 6.30; total 5.71. Para el mundo: 5.38; 4.60; 5.33; 5.32; 5.32; total 5.19.

## 3. Calibración categorial Perú 2025

Como el reporte resumido no publica los subpilares nacionales, se usa una calibración restringida a media 5.88. Vector: 8.88; 6.03; 5.07; 3.00; 6.42. Este vector solo es un **ancla interna de modelado**, no un dato oficial EIU.

## 4. Condicionamiento post-elecciones 2026

La actualización incorpora la proclamación oficial del resultado, observación internacional del proceso y fase post-electoral, evidencia de polarización/fragmentación y literatura sobre información y participación. Se evita convertir valoraciones cualitativas en supuestas probabilidades precisas; en su lugar, se traducen a shocks categoriales explícitos y auditables.

## 5. Tres escenarios

1. **Recuperación institucional y gobernabilidad negociada**: implementación de recomendaciones, coaliciones estables, fortalecimiento de capacidades y seguridad compatible con controles/garantías.
2. **Continuidad híbrida y estabilización competitiva**: competencia electoral preservada, pero reformas insuficientes, fragmentación y confianza baja.
3. **Deriva restrictiva y securitización**: excepción securitaria, erosión de controles/libertades y polarización persistente, sin suponer desaparición de elecciones competitivas.

## 6. Ecuaciones

- 2026: `x[i,2026] = clip(x[i,2025] + shock[i,s], 0, 10)`
- 2027–2030: `x[i,t] = clip(x[i,t-1] + growth[i,s] * decay[t], 0, 10)`
- `decay = {2027:1.0, 2028:0.9, 2029:0.8, 2030:0.7}`
- Total: media aritmética de cinco categorías.

## 7. Sensibilidad

10,000 trayectorias por escenario. La desviación anual por categoría toma 25% de la volatilidad histórica 2020–2024, con piso 0.04 y techo 0.20. Se presentan p10/p50/p90 como **envolvente de sensibilidad**, no como intervalo de confianza estadístico.

## 8. Limitaciones

- El EIU 2025 suministrado es un resumen; falta la tabla país/subpilar del Perú.
- Los escenarios son narrativas cuantificadas, no predicciones puntuales ni probabilidades.
- Eventos institucionales, económicos, de seguridad o constitucionales posteriores a la fecha de corte pueden invalidar coeficientes.
- La estructura del Democracy Index y sus revisiones futuras pueden modificar comparabilidad.
