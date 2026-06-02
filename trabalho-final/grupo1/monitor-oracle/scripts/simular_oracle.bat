@echo off
chcp 65001 >nul

set "PROJECT_DIR=%~dp0"
set "SCRIPT=%PROJECT_DIR%\simular_usuarios_oracle.py"

echo Pasta do projeto:
echo %PROJECT_DIR%
echo.

echo Script:
echo %SCRIPT%
echo.

if not exist "%SCRIPT%" (
    echo ERRO: Script nao encontrado.
    echo Verifique se o arquivo existe em:
    echo %SCRIPT%
    pause
    exit /b 1
)

cd /d "%PROJECT_DIR%"

echo Executando simulador...
echo.

python "%SCRIPT%"

echo.
echo Execucao finalizada.
pause