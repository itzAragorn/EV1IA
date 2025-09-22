# test.ps1
# Script de prueba para API RAG (FastAPI + LangChain)

function Call-Api($question) {
    $body = @{ q = $question } | ConvertTo-Json -Compress
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/query" `
        -Method Post `
        -ContentType "application/json; charset=utf-8" `
        -Body ([System.Text.Encoding]::UTF8.GetBytes($body))
    Write-Host "Pregunta: $question"
    Write-Host "Respuesta:" $response.answer
    Write-Host "---------------------------------------------"
}

Write-Host "🚀 Probando API RAG..."

Call-Api "¿Cuánto cloro queda en la bodega de Las Condes?"
Call-Api "¿Quién tiene turno mañana en oficinas administrativas el 2025-09-25?"
Call-Api "¿Qué productos necesitan reposición urgente en la sucursal Providencia?"
