@echo off
setlocal EnableExtensions DisableDelayedExpansion
title Publicacion auditada del Visor v2.1.0

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\publish_release.ps1" %*
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
  echo.
  echo [FALLO] La publicacion no termino. Revise el mensaje anterior.
) else (
  echo.
  echo [OK] Proceso concluido sin errores.
)

if /I not "%~1"=="-NoPause" pause
exit /b %EXIT_CODE%
