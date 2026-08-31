# Hotfix de transporte Git — 2026-08-31

## Problema observado

En Windows, el publicador podía clonar por SSH y luego fallar en una operación Git posterior con
`Permission denied (publickey)` porque Git for Windows y el agente SSH de Windows no compartían
de forma consistente la clave privada desbloqueada.

## Resolución

El publicador ya no depende de SSH. Antes de clonar:

1. valida la sesión `gh`;
2. ejecuta `gh auth setup-git --hostname github.com`;
3. desactiva prompts interactivos de credenciales con `GIT_TERMINAL_PROMPT=0`;
4. prueba `git ls-remote` sobre HTTPS;
5. clona y hace fetch/push usando `https://github.com/...`.

El token no se escribe en el repositorio, en la línea de comandos ni en archivos del release.
Git utiliza GitHub CLI como credential helper.

## Compuerta

`GIT_TRANSPORT_HTTPS_GH = PASS` es requisito antes de cualquier escritura de rama/PR.
El artículo científico y cualquier revista permanecen fuera de esta compuerta.
