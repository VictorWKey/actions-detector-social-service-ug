@echo off
echo.
echo ========================================
echo   Sistema de Reconocimiento de Actividades
echo   MODO DEMOSTRACION (Sin camara real)
echo ========================================
echo.
echo 🎮 Esta version simula el comportamiento sin hardware
echo.

python gui_demo.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ ERROR: No se pudo iniciar la demostracion
    echo.
    echo Posibles causas:
    echo - Python no esta instalado
    echo - Faltan dependencias (ejecutar: pip install -r requirements.txt)
    echo.
    pause
) else (
    echo.
    echo ✅ Demostracion cerrada correctamente
)
