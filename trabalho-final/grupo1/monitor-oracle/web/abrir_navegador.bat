@echo off
setlocal

REM =====================================================
REM Servidor local do Dashboard Oracle
REM Execute este arquivo dentro da pasta web
REM URL: http://localhost:5500
REM =====================================================

title Dashboard Oracle - Servidor Local

echo.
echo Iniciando servidor local do Dashboard Oracle...
echo.
echo Pasta atual:
cd
echo.
echo O navegador sera aberto automaticamente em:
echo http://localhost:5500
echo.
echo Para parar o servidor, pressione CTRL + C nesta janela.
echo.

REM Abre o navegador depois de 2 segundos, dando tempo do servidor iniciar
start "" powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Sleep -Seconds 2; Start-Process 'http://localhost:5500'"

REM Inicia o servidor local
python -m http.server 5500

echo.
echo Servidor finalizado.
pause

endlocal