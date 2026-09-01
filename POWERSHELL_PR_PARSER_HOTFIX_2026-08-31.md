# Hotfix PowerShell — consulta de Pull Request

## Síntoma

El publicador fallaba al iniciar incluso en modo validación con:

`ParserError: UnexpectedToken`

en la expresión jq utilizada para consultar el primer PR de una rama.

## Causa raíz

Se utilizó `\"` como escape dentro de una cadena PowerShell:

`".[0].url // \"\""`

PowerShell no usa la barra invertida como carácter de escape de comillas
dentro de strings. El carácter de escape nativo es el acento grave
(backtick). El resultado era un error de parseo antes de ejecutar
cualquier compuerta.

## Resolución

Se eliminó jq de esta consulta. El publicador ahora:

1. ejecuta `gh pr list --state open --json url`;
2. procesa el JSON con `ConvertFrom-Json`;
3. usa la primera URL si existe;
4. crea un PR borrador si la lista está vacía.

Esto evita quoting dependiente del shell y funciona tanto para el PR
existente como para el caso de creación inicial.

El hotfix no modifica datos, escenarios, semilla, corpus PRISMA,
resultados científicos ni licencias.
