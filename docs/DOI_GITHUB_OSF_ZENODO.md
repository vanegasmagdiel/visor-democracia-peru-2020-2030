# GitHub, GitHub Pages, Zenodo y OSF — política v2.1.0

## Identificadores vigentes

- DOI conceptual: https://doi.org/10.5281/zenodo.22080540
- DOI v2.0.0: https://doi.org/10.5281/zenodo.22080541
- Repositorio: https://github.com/vanegasmagdiel/visor-democracia-peru-2020-2030
- GitHub Pages: https://vanegasmagdiel.github.io/visor-democracia-peru-2020-2030/

## Estado de v2.1.0

v2.1.0-rc.5 es un candidato científico-técnico. Puede publicarse en una rama y en un
pull request, pero no debe crearse todavía el tag/release final. La release
final se habilitará cuando:

1. el entorno bloqueado reproduzca los artefactos;
2. la Fase 8 y el modelo superen sus validaciones;
3. pasen pruebas, CI, manifiesto, SHA-256 y escaneo de secretos;
4. se retire el sufijo RC y exista confirmación humana explícita.

No intervienen el estado de ningún manuscrito, revista, formulario editorial,
DOI de artículo ni la disponibilidad de OSF.

## Flujo transaccional

`PUBLICAR_VISOR_V2_1_0.bat` llama a `scripts/publish_release.ps1`.

### Modo candidato — uso actual

1. valida SHA-256 del ZIP;
2. clona el repositorio;
3. superpone el paquete;
4. reconstruye modelo y visor estático;
5. ejecuta preflight, pruebas y escaneo de secretos;
6. crea o actualiza una rama candidata;
7. abre un pull request en borrador;
8. sincroniza en OSF únicamente materiales complementarios si se suministran
   `OSF_PROJECT_ID` y `OSF_TOKEN`.

No crea release ni DOI.

### Modo final — reservado para el GO técnico del release

Con el parámetro `-PublishRelease`, el script verifica exclusivamente las
compuertas del producto, exige confirmación explícita, fusiona el PR validado,
resuelve el SHA final de `main`, crea el GitHub Release `v2.1.0` y dispara la
integración GitHub–Zenodo ya habilitada. La sincronización OSF final ocurre
únicamente después del GitHub Release, utiliza el SHA definitivo y es no
bloqueante; el DOI de versión se incorpora posteriormente cuando Zenodo lo
acuña.

## Zenodo

La integración GitHub–Zenodo está habilitada. Cada GitHub Release estable crea
un nuevo DOI de versión y conserva el DOI conceptual. Un prerelease o rama no
debe utilizarse para acuñar un objeto científico definitivo.

## OSF

OSF conserva protocolo, decisiones y materiales no ejecutables. No debe
duplicar el release completo de Zenodo. Véase `docs/OSF_COMPLEMENT.md`.
