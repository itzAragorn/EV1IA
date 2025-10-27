"""
API Simple para Pruebas - CleanPro
==================================
Versión simplificada para demostración sin problemas de compatibilidad
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

app = FastAPI(
    title="CleanPro Agent API - Demo",
    description="API de demostración para agentes CleanPro",
    version="2.0.0-demo"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = "demo_session"

class CrewRequest(BaseModel):
    objective: str
    flow_type: Optional[str] = "investigacion_completa"
    session_id: Optional[str] = "crew_demo"

class PlanRequest(BaseModel):
    plan_id: str
    objective: str
    context: Dict[str, Any]

# Estado simulado del sistema
system_state = {
    "agents_active": 0,
    "crews_active": 0,
    "plans_active": 0,
    "sessions": {},
    "start_time": datetime.now().isoformat()
}

# ============================================================================
# ENDPOINTS DE DEMOSTRACIÓN
# ============================================================================

@app.get("/")
def root():
    """Información del API de demostración."""
    return {
        "name": "CleanPro Agent API - Demo Version",
        "version": "2.0.0-demo",
        "description": "API de demostración para sistema de agentes CleanPro",
        "status": "demo_mode",
        "note": "Esta es una versión simplificada para pruebas y demostración",
        "endpoints": {
            "agent": "/agent/query - Simula agente individual",
            "crew": "/crew/execute - Simula sistema multi-agente",
            "planning": "/planning/create - Simula planificación adaptativa",
            "health": "/health - Estado del sistema"
        }
    }

@app.get("/health")
def health_check():
    """Estado del sistema."""
    return {
        "status": "healthy",
        "mode": "demo",
        "uptime": datetime.now().isoformat(),
        "systems": {
            "individual_agents": "simulated",
            "multi_agent_crews": "simulated", 
            "adaptive_planning": "simulated",
            "memory_system": "simulated"
        },
        "stats": system_state
    }

@app.post("/agent/query")
def agent_query(request: QueryRequest):
    """Simula consulta a agente individual."""
    
    # Actualizar estado
    system_state["agents_active"] += 1
    
    # Simular procesamiento basado en la consulta
    query_lower = request.query.lower()
    
    # INVENTARIO/STOCK - Solo Las Condes
    if any(palabra in query_lower for palabra in ["inventario", "stock", "productos", "equipos", "suministros"]):
        if "las condes" in query_lower or "condes" in query_lower:
            response = {
                "response": """**Análisis de Inventario CleanPro - Las Condes**

🔍 **Consulta RAG Realizada**: Revisé la base de conocimientos sobre inventario de Las Condes.

📊 **Hallazgos Principales**:
- Productos de limpieza: Stock óptimo en detergentes industriales
- Equipos: 3 aspiradoras industriales operativas, 1 en mantención
- Suministros: Nivel bajo en trapos de microfibra (restock recomendado)

⚡ **Herramientas Utilizadas**: 
- `rag_consulta`: Búsqueda vectorial en base de conocimientos
- `analisis_datos`: Procesamiento de inventory_las_condes.csv

💡 **Recomendación**: Programar reabastecimiento de microfibra para próxima semana.""",
                "tools_used": ["rag_consulta", "analisis_datos"],
                "session_id": request.session_id,
                "memory_strategy": "buffer",
                "processing_time": "2.3s"
            }
        else:
            # Pregunta sobre inventario pero sin especificar Las Condes o con otra ubicación
            ubicaciones_detectadas = []
            if "rancagua" in query_lower:
                ubicaciones_detectadas.append("Rancagua")
            if "santiago" in query_lower:
                ubicaciones_detectadas.append("Santiago") 
            if "valparaiso" in query_lower or "valparaíso" in query_lower:
                ubicaciones_detectadas.append("Valparaíso")
            if "providencia" in query_lower:
                ubicaciones_detectadas.append("Providencia")
            if "ñuñoa" in query_lower:
                ubicaciones_detectadas.append("Ñuñoa")
            
            if ubicaciones_detectadas:
                # Pregunta específica sobre otra ubicación
                ubicacion = ubicaciones_detectadas[0]
                response = {
                    "response": f"""**Información No Disponible - {ubicacion}**

⚠️ **Limitación de Datos**: Lo siento, no tengo acceso a información de inventario/stock para {ubicacion}.

📊 **Datos Disponibles**:
- ✅ Inventario de **Las Condes** (inventory_las_condes.csv)
- ✅ Turnos de **Septiembre** (turnos_septiembre.csv)

🔍 **Consulta RAG**: Realicé búsqueda en la base de conocimientos, pero no encontré datos para {ubicacion}.

💡 **Sugerencia**: Pregúntame sobre "stock en Las Condes" para obtener información detallada.""",
                    "tools_used": ["rag_consulta"],
                    "session_id": request.session_id,
                    "memory_strategy": "buffer",
                    "processing_time": "1.1s"
                }
            else:
                # Pregunta general sobre inventario sin especificar ubicación
                response = {
                    "response": """**Consulta de Inventario/Stock - Ubicación Requerida**

🔍 **Consulta RAG**: Detecté una consulta sobre inventario/stock, pero necesito que especifiques la ubicación.

� **Datos Disponibles**:
- ✅ Inventario de **Las Condes** (inventory_las_condes.csv)
- ✅ Turnos de **Septiembre** (turnos_septiembre.csv)

⚠️ **Aclaración Necesaria**: Solo tengo información de inventario para Las Condes.

💡 **Consultas Válidas**:
- "¿Hay stock en Las Condes?"
- "¿Qué inventario hay en Las Condes?"
- "¿Cuál es el estado del inventario de Las Condes?"

🔍 **Resultado**: Para obtener información específica, por favor menciona "Las Condes".""",
                    "tools_used": ["rag_consulta", "adaptacion_contextual"],
                    "session_id": request.session_id,
                    "memory_strategy": "buffer",
                    "processing_time": "1.3s"
                }
    
    # TURNOS/PERSONAL - Solo Septiembre
    elif any(palabra in query_lower for palabra in ["turno", "personal", "empleado", "trabajador", "horario"]):
        if "septiembre" in query_lower or not any(mes in query_lower for mes in ["octubre", "noviembre", "diciembre", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto"]):
            response = {
                "response": """**Análisis de Turnos Septiembre**

👥 **Consulta de Personal**: Información procesada sobre turnos de septiembre.

📋 **Datos Principales**:
- Total empleados activos: 24 personas
- Turnos mañana: 12 personas (6:00-14:00)
- Turnos tarde: 8 personas (14:00-22:00)  
- Turnos noche: 4 personas (22:00-6:00)

⚡ **Herramientas Utilizadas**:
- `rag_consulta`: Búsqueda en base de turnos
- `analisis_datos`: Análisis de turnos_septiembre.csv

📈 **Insight**: Mayor demanda en turnos de mañana, considerar redistribución.""",
                "tools_used": ["rag_consulta", "analisis_datos"],  
                "session_id": request.session_id,
                "memory_strategy": "window",
                "processing_time": "1.8s"
            }
        else:
            # Pregunta sobre turnos de otro mes
            mes_mencionado = "mes solicitado"
            if "octubre" in query_lower:
                mes_mencionado = "octubre"
            elif "noviembre" in query_lower:
                mes_mencionado = "noviembre"
            elif "diciembre" in query_lower:
                mes_mencionado = "diciembre"
            
            response = {
                "response": f"""**Información No Disponible - Turnos {mes_mencionado.title()}**

⚠️ **Limitación de Datos**: Lo siento, no tengo acceso a información de turnos para {mes_mencionado}.

📊 **Datos Disponibles**:
- ✅ Inventario de **Las Condes** (inventory_las_condes.csv)
- ✅ Turnos de **Septiembre** (turnos_septiembre.csv)

🔍 **Consulta RAG**: Realicé búsqueda en la base de conocimientos, pero no encontré datos de turnos para {mes_mencionado}.

💡 **Sugerencia**: Pregúntame sobre "turnos de septiembre" para obtener información detallada.""",
                "tools_used": ["rag_consulta"],
                "session_id": request.session_id,
                "memory_strategy": "buffer",
                "processing_time": "1.0s"
            }
        
    elif "reporte" in query_lower or "análisis" in query_lower:
        response = {
            "response": """**Reporte Ejecutivo CleanPro**

📄 **Generación de Documentación**: Reporte estructurado basado en datos disponibles.

🎯 **Componentes del Reporte**:
1. **Análisis de Inventario Las Condes**: Evaluación de stock y equipos
2. **Análisis de Turnos Septiembre**: Distribución y patrones de personal
3. **Recomendaciones**: Estrategias basadas en datos disponibles
4. **Plan de Acción**: Pasos siguientes priorizados

⚡ **Herramientas Utilizadas**:
- `rag_consulta`: Acceso a datos disponibles
- `escritura_reporte`: Generación estructurada de documentos
- `razonamiento_decision`: Análisis estratégico
- `planificacion_estrategica`: Desarrollo de roadmap

✅ **Estado**: Reporte basado en datos de Las Condes (inventario) y Septiembre (turnos).""",
            "tools_used": ["rag_consulta", "escritura_reporte", "razonamiento_decision", "planificacion_estrategica"],
            "session_id": request.session_id,
            "memory_strategy": "summary",
            "processing_time": "4.1s"
        }
    
    else:
        response = {
            "response": f"""**Consulta General - Agente CleanPro**

🤖 **Procesamiento**: He analizado tu consulta: "{request.query}"

📊 **Datos Disponibles en Mi Base de Conocimientos**:
- ✅ **Inventario de Las Condes** (productos, equipos, suministros)
- ✅ **Turnos de Septiembre** (distribución de personal y horarios)

🛠️ **Capacidades Disponibles**:
- 🔍 Consulta RAG sobre inventarios y turnos
- ✍️ Generación de reportes y análisis
- 🧠 Razonamiento y toma de decisiones
- 📋 Planificación estratégica

⚠️ **Limitaciones**: Solo tengo información específica sobre Las Condes (inventario) y Septiembre (turnos).

💡 **Sugerencias de Consulta**:
- "¿Hay inventario en Las Condes?"
- "Dame los turnos de septiembre"
- "Genera un reporte de análisis"
- "¿Qué recomendaciones tienes?"

🔍 **Consulta RAG**: Realicé búsqueda pero no encontré información específica para tu consulta.""",
            "tools_used": ["rag_consulta", "adaptacion_contextual"],
            "session_id": request.session_id, 
            "memory_strategy": "buffer",
            "processing_time": "1.5s"
        }
    
    # Guardar en sesión simulada
    if request.session_id not in system_state["sessions"]:
        system_state["sessions"][request.session_id] = []
    
    system_state["sessions"][request.session_id].append({
        "query": request.query,
        "response": response["response"],
        "timestamp": datetime.now().isoformat(),
        "tools_used": response["tools_used"]
    })
    
    return response

@app.post("/crew/execute")  
def execute_crew(request: CrewRequest):
    """Simula ejecución de sistema multi-agente."""
    
    # Actualizar estado
    system_state["crews_active"] += 1
    
    # Simular flujo multi-agente
    crew_result = {
        "status": "completed",
        "flow_type": request.flow_type,
        "objective": request.objective,
        "result": {
            "investigacion": {
                "agente": "Investigador de Datos CleanPro",
                "hallazgos": [
                    "Datos de inventario procesados: 156 items analizados",
                    "Patrones identificados en turnos: Picos de demanda mañanas",
                    "Eficiencia operativa: 87% promedio en septiembre"
                ],
                "fuentes": ["inventory_las_condes.csv", "turnos_septiembre.csv", "base_conocimientos_rag"]
            },
            "analisis": {
                "agente": "Analista Estratégico CleanPro", 
                "evaluacion": "Operaciones estables con oportunidades de optimización",
                "criterios_decision": ["Eficiencia", "Costo", "Calidad", "Tiempo"],
                "recomendacion": "Implementar redistribución de turnos y restock planificado"
            },
            "documentacion": {
                "agente": "Especialista en Documentación CleanPro",
                "entregables": [
                    "Reporte ejecutivo de operaciones Q4",
                    "Plan de optimización de recursos", 
                    "Dashboard de métricas operativas"
                ],
                "formato": "Documentación técnica estructurada"
            },
            "coordinacion": {
                "agente": "Coordinador de Proyectos CleanPro",
                "flujo_ejecutado": "Secuencial con dependencias",
                "tiempo_total": "8.7 minutos",
                "integracion": "Exitosa entre todos los especialistas"
            },
            "agentes_utilizados": ["Investigador", "Analista", "Documentador", "Coordinador"],
            "herramientas_empleadas": ["rag_consulta", "analisis_datos", "razonamiento_decision", "escritura_reporte"],
            "metricas": {
                "tareas_completadas": 12,
                "colaboraciones": 8, 
                "tiempo_ejecucion": "8m 42s"
            }
        },
        "session_id": request.session_id,
        "timestamp": datetime.now().isoformat()
    }
    
    return crew_result

@app.post("/planning/create")
def create_adaptive_plan(request: PlanRequest):
    """Simula creación de plan adaptativo."""
    
    # Actualizar estado
    system_state["plans_active"] += 1
    
    # Simular planificación adaptativa
    plan_response = {
        "plan_id": request.plan_id,
        "status": "created",
        "objective": request.objective,
        "context_analysis": {
            "recursos_disponibles": request.context.get("recursos", []),
            "restricciones_tiempo": request.context.get("tiempo", {}),
            "complejidad_estimada": "media-alta"
        },
        "strategy_selected": "planificacion_jerarquica_adaptativa",
        "tareas_generadas": [
            {
                "id": "tarea_001",
                "descripcion": "Análisis inicial de requerimientos",
                "prioridad": "alta",
                "estimacion_tiempo": 30,
                "dependencias": []
            },
            {
                "id": "tarea_002", 
                "descripcion": "Recopilación de datos organizacionales",
                "prioridad": "alta",
                "estimacion_tiempo": 45,
                "dependencias": ["tarea_001"]
            },
            {
                "id": "tarea_003",
                "descripcion": "Desarrollo de estrategia de implementación", 
                "prioridad": "media",
                "estimacion_tiempo": 60,
                "dependencias": ["tarea_002"]
            }
        ],
        "adaptaciones_configuradas": [
            "adaptacion_por_tiempo",
            "adaptacion_por_recursos", 
            "adaptacion_por_feedback",
            "adaptacion_por_complejidad"
        ],
        "metricas_seguimiento": {
            "progreso": "0%",
            "tiempo_transcurrido": "0m",
            "recursos_utilizados": "0%"
        },
        "timestamp": datetime.now().isoformat()
    }
    
    return plan_response

@app.get("/agent/sessions/{session_id}/info")
def get_session_info(session_id: str):
    """Obtiene información de sesión."""
    
    session_data = system_state["sessions"].get(session_id, [])
    
    return {
        "session_id": session_id,
        "message_count": len(session_data),
        "memory_strategy": "adaptativo" if len(session_data) > 12 else ("window" if len(session_data) > 4 else "buffer"),
        "tools_available": [
            "rag_consulta", "escritura_reporte", "analisis_datos",
            "razonamiento_decision", "planificacion_estrategica", "adaptacion_contextual"
        ],
        "last_activity": session_data[-1]["timestamp"] if session_data else None,
        "interaction_history": session_data[-3:] if len(session_data) > 3 else session_data
    }

@app.get("/systems/cleanup")
def cleanup_system():
    """Limpia el estado del sistema."""
    global system_state
    
    sessions_cleared = len(system_state["sessions"])
    
    system_state = {
        "agents_active": 0,
        "crews_active": 0, 
        "plans_active": 0,
        "sessions": {},
        "start_time": datetime.now().isoformat()
    }
    
    return {
        "status": "cleaned",
        "sessions_cleared": sessions_cleared,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)