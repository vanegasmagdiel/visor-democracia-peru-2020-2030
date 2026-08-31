@echo off
setlocal EnableExtensions DisableDelayedExpansion
title Publicacion auditada del Visor v2.1.0

set "PS_SCRIPT=%~dp0scripts\publish_release.ps1"
if not exist "%PS_SCRIPT%" set "PS_SCRIPT=%~dp0PUBLICAR_VISOR_V2_1_0.ps1"

if not exist "%PS_SCRIPT%" (
  echo.
  echo [ERROR] Falta el motor de publicacion PowerShell.
  echo Coloque PUBLICAR_VISOR_V2_1_0.ps1 junto a este BAT,
  echo o ejecute el BAT desde la raiz extraida del paquete.
  set "EXIT_CODE=2"
  goto :finish
)

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
