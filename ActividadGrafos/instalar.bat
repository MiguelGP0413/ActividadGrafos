@echo off
echo.
echo ==========================================
echo  Mapa de Afinidades Electorales
echo  Instalador de Dependencias
echo ==========================================
echo.

REM Verificar si pip está disponible
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado o no está en PATH
    pause
    exit /b 1
)

echo Instalando dependencias...
echo.

python -m pip install -r requirements.txt

if errorlevel 1 (
    echo Error durante la instalación
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Instalación completada exitosamente!
echo.
echo Para ejecutar la aplicación, utiliza:
echo   streamlit run app.py
echo.
pause
