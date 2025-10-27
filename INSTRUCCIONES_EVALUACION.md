# 🚀 Instrucciones de Ejecución - Sistema CleanPro Intelligent Agents

## ⚡ Inicio Rápido para Evaluadores

### 📋 Prerrequisitos
- Python 3.8+ instalado
- Token de GitHub con acceso a GitHub Models API
- Terminal/PowerShell con acceso a internet

### 🔧 Configuración Inicial (5 minutos)

1. **Instalar dependencias**:
```bash
pip install -r requeriments.txt
```

2. **Configurar variables de entorno**:
Crear archivo `.env` en la raíz con:
```bash
OPENAI_BASE_URL="https://models.inference.ai.azure.com"
OPENAI_EMBEDDINGS_URL="https://models.github.ai/inference"
OPENAI_API_KEY="tu_github_token_aquí"
GITHUB_TOKEN="tu_github_token_aquí"
```

3. **Preparar base de datos vectorial**:
```bash
python src/ingestion/ingest_all.py
```

### 🎯 Ejecución de Demostraciones

#### 🤖 Demo Completa Automatizada (Recomendado)
```bash
python demo_flujos_automatizados.py
```
**Tiempo estimado**: 5-10 minutos  
**Demuestra**: Todos los IL (IL2.1, IL2.2, IL2.3, IL2.4)

#### 🌐 Interfaz Web Interactiva

**OPCIÓN A - Script Automatizado (Windows):**
```bash
# Terminal 1 - API
.\iniciar_api.bat

# Terminal 2 - Interfaz
streamlit run app_streamlit.py
```

**OPCIÓN B - Manual:**
```bash
# Terminal 1 - API
cd src/api
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Interfaz
streamlit run app_streamlit.py
```

**Acceder**: `http://localhost:8501`

#### 🧪 Validación Automatizada del Sistema
```bash
python validar_sistema.py
```
**Tiempo estimado**: 2-3 minutos  
**Verifica**: Configuración, archivos, conectividad, funcionalidad completa

### 🧪 Pruebas de Validación por IL

#### ✅ IL2.1 - Agentes Funcionales
**Consulta de ejemplo**:
```bash
curl -X POST "http://localhost:8000/agent/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Analiza el inventario y genera un reporte ejecutivo", "session_id": "eval_test_1"}'
```

**Validar**: Respuesta incluye uso de múltiples herramientas (rag_consulta, escritura_reporte, etc.)

#### ✅ IL2.2 - Memoria Conversacional
**Secuencia de consultas**:
```bash
# Primera consulta
curl -X POST "http://localhost:8000/agent/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "¿Cuál es el estado del inventario?", "session_id": "memoria_test"}'

# Segunda consulta (debe recordar contexto)
curl -X POST "http://localhost:8000/agent/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Basándote en ese análisis, ¿qué recomiendas?", "session_id": "memoria_test"}'
```

**Validar**: Segunda respuesta hace referencia al análisis previo.

#### ✅ IL2.3 - Planificación Adaptativa
**Crear plan**:
```bash
curl -X POST "http://localhost:8000/planning/create" \
  -H "Content-Type: application/json" \
  -d '{
    "plan_id": "eval_plan_1", 
    "objective": "Optimizar operaciones CleanPro",
    "context": {
      "recursos": ["equipo_analisis", "base_datos"],
      "tiempo": {"deadline": 300}
    }
  }'
```

**Simular cambio de contexto**:
```bash
curl -X PUT "http://localhost:8000/planning/plans/eval_plan_1/context" \
  -H "Content-Type: application/json" \
  -d '{
    "recursos": ["base_datos"],
    "tiempo": {"deadline": 150},
    "feedback": ["Acelerar proceso", "Recursos limitados"]
  }'
```

**Validar**: Respuesta incluye adaptaciones realizadas.

#### ✅ IL2.4 - Documentación e Integración
**Verificar documentación**:
- Abrir `README.md` - Documentación técnica completa
- Revisar diagramas de arquitectura Mermaid
- Explorar estructura de archivos documentada

### 📊 Casos de Uso Organizacionales

#### Caso 1: Análisis de Inventario
```python
# En interfaz web o API
"Consulta el inventario de Las Condes, identifica productos con stock bajo y genera un reporte con recomendaciones de reabastecimiento."
```

#### Caso 2: Optimización Multi-Agente
```bash
curl -X POST "http://localhost:8000/crew/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "objective": "Desarrollar estrategia de optimización de turnos Q1 2025",
    "flow_type": "planificacion_estrategica",
    "restrictions": ["Presupuesto limitado", "Regulaciones laborales"],
    "resources": ["Datos históricos", "Equipo de planificación"]
  }'
```

#### Caso 3: Flujo Integrado Completo
```python
# Ejecutar en demo_flujos_automatizados.py - función demo_integracion_sistemas()
# Demuestra: Agente individual → Multi-agente → Planificación → Reporte final
```

### 🔍 Verificación de Funcionalidades

#### Estado del Sistema
```bash
curl http://localhost:8000/health
```
**Esperado**: Status "healthy" con contadores de sistemas activos.

#### Información de Sesiones
```bash
curl http://localhost:8000/agent/sessions/eval_test_1/info
```
**Esperado**: Datos de memoria, herramientas disponibles y estadísticas.

#### Cleanup (Opcional)
```bash
curl http://localhost:8000/systems/cleanup
```

### 🚨 Troubleshooting

#### Error de Autenticación
```
AuthenticationError: Incorrect API key provided
```
**Solución**: Verificar token de GitHub en archivo `.env`

#### Error de Base de Datos
```
No se pudo acceder a la base de conocimientos
```
**Solución**: Ejecutar `python src/ingestion/ingest_all.py`

#### Error de Puerto
```
Address already in use
```
**Solución**: Cambiar puerto o terminar procesos:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID [PID_NUMBER] /F

# Linux/Mac  
lsof -ti:8000 | xargs kill -9
```

### 📁 Estructura de Archivos Clave

```
├── src/agents/
│   ├── langchain_agent.py      # IL2.1 - Agente individual
│   ├── crewai_orchestration.py # IL2.3 - Multi-agente
│   ├── memory/                 # IL2.2 - Sistema de memoria
│   ├── tools/                  # IL2.1 - Herramientas integradas
│   └── planning/               # IL2.3 - Planificación adaptativa
├── src/api/app.py              # API completa
├── app_streamlit.py            # Interfaz web
├── demo_flujos_automatizados.py # Demostraciones IL2.1-IL2.4
└── README.md                   # IL2.4 - Documentación técnica
```

### ⏱️ Tiempos Estimados de Evaluación

- **Configuración inicial**: 5 minutos
- **Demo automatizada completa**: 10 minutos
- **Pruebas de API individuales**: 5 minutos por IL
- **Exploración de interfaz web**: 10 minutos
- **Revisión de documentación**: 15 minutos

**Total estimado para evaluación completa**: 45-60 minutos

### 🎯 Puntos de Evaluación Clave

1. **IL2.1**: Verificar integración de herramientas en respuestas del agente
2. **IL2.2**: Confirmar continuidad conversacional entre consultas
3. **IL2.3**: Observar adaptaciones en planificación por cambios de contexto  
4. **IL2.4**: Revisar completitud de documentación y diagramas

### 📞 Soporte de Evaluación

En caso de problemas durante la evaluación:
1. Verificar configuración de `.env`
2. Revisar logs en terminal
3. Consultar sección Troubleshooting en README.md
4. Ejecutar `python demo_flujos_automatizados.py` para verificación rápida

---

**¡Sistema listo para evaluación completa de todos los Indicadores de Logro!** 🚀