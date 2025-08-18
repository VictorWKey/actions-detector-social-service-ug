@echo off
echo.
echo ========================================
echo   Sistema de Reconocimiento de Actividades
echo   Interfaz Grafica - Version GUI
echo ========================================
echo.

echo 🔍 Verificando dependencias...
python check_dependencies.py

echo.
echo 🚀 Iniciando aplicacion GUI...
echo.

python gui_main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ ERROR: No se pudo iniciar la aplicacion
    echo.
    echo Posibles causas:
    echo - Python no esta instalado
    echo - Faltan dependencias (ejecutar: pip install -r requirements.txt)
    echo - Camara RealSense no conectada
    echo.
    echo Ejecuta check_dependencies.py para mas detalles
    echo.
    pause
) else (
    echo.
    echo ✅ Aplicacion cerrada correctamente
)
