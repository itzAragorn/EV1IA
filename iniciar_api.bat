@echo off
cd /d "c:\Users\Nico Osses\Documents\Materia\IA\EV1"
set OPENAI_BASE_URL=https://models.inference.ai.azure.com

REM Verificar si las variables de entorno están configuradas
if not defined GITHUB_TOKEN (
    echo ERROR: GITHUB_TOKEN no está configurado.
    echo Por favor configura tu token de GitHub:
    echo set GITHUB_TOKEN=tu_github_token_aqui
    echo set OPENAI_API_KEY=tu_github_token_aqui
    pause
    exit /b 1
)

set OPENAI_API_KEY=%GITHUB_TOKEN%
echo Iniciando API CleanPro en puerto 8000...
echo Usando GITHUB_TOKEN configurado en variables de entorno
python -m uvicorn demo_api:app --reload --port 8000
pause