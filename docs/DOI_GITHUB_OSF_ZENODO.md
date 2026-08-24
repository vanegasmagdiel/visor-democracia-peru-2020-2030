# Publicación, preservación y DOI — ruta recomendada (verificada 2026-08-19)

## Ruta A — recomendada: GitHub + Zenodo

1. Subir esta carpeta a un repositorio GitHub.
2. Activar GitHub Pages desde la rama principal y la carpeta `/docs`; `docs/index.html` ya es el punto de entrada estático.
3. Conectar la cuenta GitHub con Zenodo y habilitar el repositorio en la integración de software.
4. Crear una release GitHub `v2.0.0`. Zenodo puede archivar la release habilitada y generar el registro persistente.
5. Zenodo asigna DOI al publicar el depósito. También permite reservar el DOI antes de publicar si se desea incorporarlo a metadatos/figuras.
6. Actualizar `CITATION.cff`, `.zenodo.json`, `datacite.json`, `codemeta.json` y README con el DOI emitido.

Documentación oficial:
- Zenodo GitHub integration: https://help.zenodo.org/docs/github/
- Archive GitHub release: https://help.zenodo.org/docs/github/archive-software/github-upload/
- Reserve DOI: https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/
- GitHub Pages publishing source: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Ruta B — OSF

Para preservación académica, subir la release y metadatos a OSF o crear una **Registration** pública. La documentación vigente de OSF indica que los registros públicos reciben DOI. Mantener sincronizados título, autores, versión, licencia y recursos relacionados.

Documentación oficial:
- OSF Registrations: https://help.osf.io/article/330-welcome-to-registrations
- OSF metadata: https://help.osf.io/article/571-add-metadata-to-your-osf-registration

## Recomendación de versionado

- Repositorio vivo: GitHub (`main`).
- Versión citable: GitHub Release `v2.0.0` + Zenodo DOI de versión.
- DOI conceptual: usarlo para citar el proyecto a través de versiones cuando Zenodo lo asigne.
- Materiales/registro de investigación: OSF, enlazando el DOI de Zenodo cuando corresponda.

**Regla:** no escribir ni inventar un DOI antes de que Zenodo/OSF lo emita o lo reserve formalmente.
