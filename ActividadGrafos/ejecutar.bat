@echo off
echo.
echo ==========================================
echo  Mapa de Afinidades Electorales
echo  Iniciando Aplicación...
echo ==========================================
echo.

REM Verificar si streamlit está disponible
python -m streamlit --version >nul 2>&1
if errorlevel 1 (
    echo Error: Streamlit no está instalado.
    echo Por favor ejecuta 'instalar.bat' primero.
    pause
    exit /b 1
)

echo Abriendo navegador en http://localhost:8501
echo (Presiona Ctrl+C para detener la aplicación)
echo.

python -m streamlit run app.py

pause
