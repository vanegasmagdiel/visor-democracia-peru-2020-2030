# Hotfix de detección/creación de Pull Request — 2026-08-31

## Síntoma

Después de publicar correctamente la rama `codex/v2.1.0-rc.5-technical-refactor`,
el publicador se detenía con:

`no pull requests found for branch "codex/v2.1.0-rc.5-technical-refactor"`

## Causa

`gh pr view <branch>` devuelve código distinto de cero cuando aún no existe un PR.
En el entorno Windows auditado, ese estado se elevó como fallo antes de alcanzar
la rama lógica que debía ejecutar `gh pr create`.

## Solución

La detección usa ahora:

`gh pr list --head <branch> --state all --json url`

Una lista vacía es un resultado normal con código 0. Si no existe PR, el
publicador continúa y crea un PR borrador. Si ya existe, reutiliza su URL.

Este cambio no modifica datos, modelos, resultados, manifiestos científicos ni
metadatos de investigación, salvo el inventario/checksum necesario para reflejar
el propio hotfix.
