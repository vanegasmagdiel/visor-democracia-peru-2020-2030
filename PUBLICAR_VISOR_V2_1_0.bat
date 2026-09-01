@echo off
setlocal EnableExtensions DisableDelayedExpansion
title Publicacion auditada del Visor v2.1.0

set "PS_SCRIPT=%~dp0scripts\publish_release.ps1"
set "CI_RESOLVER=%~dp0scripts\resolve_ci_run.ps1"
if not exist "%PS_SCRIPT%" set "PS_SCRIPT=%~dp0PUBLICAR_VISOR_V2_1_0.ps1"

if not exist "%PS_SCRIPT%" (
  echo.
  echo [ERROR] Falta el motor de publicacion PowerShell.
  echo Coloque PUBLICAR_VISOR_V2_1_0.ps1 junto a este BAT,
  echo o ejecute el BAT desde la raiz extraida del paquete.
  set "EXIT_CODE=2"
  goto :finish
)

if not exist "%CI_RESOLVER%" (
  echo.
  echo [ERROR] Falta scripts\resolve_ci_run.ps1.
  set "EXIT_CODE=2"
  goto :finish
)

echo [CHECK] Validando sintaxis PowerShell antes de ejecutar...
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -Command "$files=@($env:PS_SCRIPT,$env:CI_RESOLVER); $all=@(); foreach($f in $files){$e=@();$t=@();[void][System.Management.Automation.Language.Parser]::ParseFile($f,[ref]$t,[ref]$e); $all += $e}; if($all.Count -gt 0){foreach($x in $all){Write-Host ('[PARSER] ' + $x.Message) -ForegroundColor Red}; exit 2}"
if errorlevel 1 (
  set "EXIT_CODE=2"
  goto :finish
)
echo [OK] Sintaxis PowerShell valida.

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%PS_SCRIPT%" %*
set "EXIT_CODE=%ERRORLEVEL%"

:finish
if not "%EXIT_CODE%"=="0" (
  echo.
  echo [FALLO] La publicacion no termino. Revise el mensaje anterior.
) else (
  echo.
  echo [OK] Proceso concluido sin errores.
)

if /I not "%~1"=="-NoPause" pause
exit /b %EXIT_CODE%
