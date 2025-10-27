import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

# Importar sistemas existentes
from src.chains.rag_chain import get_rag_chain

# Importar nuevos sistemas de agentes
from src.agents.langchain_agent import create_cleanpro_agent
from src.agents.crewai_orchestration import create_cleanpro_crew
from src.agents.planning.adaptive_planning import planning_manager, ContextoEjecucion

load_dotenv()

app = FastAPI(
    title="CleanPro Intelligent Agent API",
    description="API avanzada con agentes inteligentes para automatización organizacional",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sistemas existentes
rag_chain = get_rag_chain()

# Nuevos sistemas de agentes
agents_cache = {}  # Cache de agentes por sesión
crews_cache = {}   # Cache de crews por sesión


# Modelos de petición y respuesta
class Query(BaseModel):
    q: str

class AgentQuery(BaseModel):
    query: str = Field(description="Consulta para el agente")
    session_id: str = Field(default="default", description="ID de sesión para memoria persistente")
    mode: str = Field(default="individual", description="Modo: individual, crew, planning")

class CrewTask(BaseModel):
    objective: str = Field(description="Objetivo del flujo de trabajo")
    flow_type: str = Field(default="investigacion_completa", description="Tipo de flujo: investigacion_completa, planificacion_estrategica, personalizado")
    restrictions: Optional[List[str]] = Field(default=None, description="Restricciones del proyecto")
    resources: Optional[List[str]] = Field(default=None, description="Recursos disponibles")
    session_id: str = Field(default="crew_default", description="ID de sesión del crew")

class PlanningRequest(BaseModel):
    plan_id: str = Field(description="ID único del plan")
    objective: str = Field(description="Objetivo del plan")
    context: Dict[str, Any] = Field(default={}, description="Contexto de ejecución")
    session_id: str = Field(default="planning_default", description="ID de sesión de planificación")


# ============================================================================
# ENDPOINTS ORIGINALES (compatibilidad hacia atrás)
# ============================================================================

@app.post("/query")
def query_rag(body: Query):
    """Endpoint original de consulta RAG (mantenido para compatibilidad)."""
    result = rag_chain.invoke({"query": body.q})
    return {"answer": result["result"]}


# ============================================================================
# ENDPOINTS DE AGENTE INDIVIDUAL (LangChain)
# ============================================================================

@app.post("/agent/query")
def query_agent(body: AgentQuery):
    """Consulta un agente individual con memoria conversacional."""
    try:
        # Obtener o crear agente para la sesión
        if body.session_id not in agents_cache:
            agents_cache[body.session_id] = create_cleanpro_agent(body.session_id)
        
        agent = agents_cache[body.session_id]
        
        # Procesar consulta
        result = agent.process_query(body.query)
        
        return {
            "status": "success",
            "response": result["response"],
            "session_id": result["session_id"], 
            "tools_used": result.get("tools_used", []),
            "memory_summary": result.get("memory_summary", ""),
            "intermediate_steps": len(result.get("intermediate_steps", []))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en agente individual: {str(e)}")


@app.get("/agent/sessions/{session_id}/info")
def get_agent_session_info(session_id: str):
    """Obtiene información de una sesión de agente."""
    if session_id not in agents_cache:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    agent = agents_cache[session_id]
    return agent.get_session_info()


@app.delete("/agent/sessions/{session_id}")
def reset_agent_session(session_id: str):
    """Reinicia una sesión de agente."""
    if session_id in agents_cache:
        agents_cache[session_id].reset_session()
        return {"status": "success", "message": f"Sesión {session_id} reiniciada"}
    else:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")


# ============================================================================
# ENDPOINTS DE SISTEMA MULTI-AGENTE (CrewAI)
# ============================================================================

@app.post("/crew/execute")
def execute_crew_task(body: CrewTask):
    """Ejecuta un flujo de trabajo multi-agente."""
    try:
        # Obtener o crear crew para la sesión
        if body.session_id not in crews_cache:
            crews_cache[body.session_id] = create_cleanpro_crew(body.session_id)
        
        crew = crews_cache[body.session_id]
        
        # Ejecutar flujo según el tipo
        if body.flow_type == "investigacion_completa":
            result = crew.investigacion_completa(body.objective)
            
        elif body.flow_type == "planificacion_estrategica":
            result = crew.planificacion_estrategica(
                objetivo=body.objective,
                restricciones=body.restrictions or [],
                recursos=body.resources or []
            )
            
        else:
            raise HTTPException(status_code=400, detail=f"Tipo de flujo no soportado: {body.flow_type}")
        
        return {
            "status": "success",
            "result": result,
            "flow_type": body.flow_type,
            "session_id": body.session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en sistema multi-agente: {str(e)}")


@app.get("/crew/sessions/{session_id}/info")
def get_crew_info(session_id: str):
    """Obtiene información del crew."""
    if session_id not in crews_cache:
        raise HTTPException(status_code=404, detail="Crew no encontrado")
    
    crew = crews_cache[session_id]
    return crew.get_crew_info()


# ============================================================================
# ENDPOINTS DE PLANIFICACIÓN ADAPTATIVA
# ============================================================================

@app.post("/planning/create")
def create_adaptive_plan(body: PlanningRequest):
    """Crea un nuevo plan adaptativo."""
    try:
        plan = planning_manager.crear_plan(body.plan_id, body.objective)
        
        # Si hay contexto, actualizarlo
        if body.context:
            contexto = ContextoEjecucion(
                recursos_disponibles=body.context.get("recursos", []),
                restricciones_tiempo=body.context.get("tiempo", {}),
                condiciones_externas=body.context.get("condiciones", {}),
                feedback_usuario=body.context.get("feedback", []),
                metricas_performance=body.context.get("metricas", {})
            )
            plan.actualizar_contexto(contexto)
        
        return {
            "status": "success",
            "plan_id": body.plan_id,
            "objective": body.objective,
            "plan_data": plan.exportar_plan()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando plan: {str(e)}")


@app.get("/planning/plans")
def list_plans():
    """Lista todos los planes activos."""
    return {
        "status": "success",
        "plans": planning_manager.listar_planes()
    }


@app.get("/planning/plans/{plan_id}")
def get_plan_details(plan_id: str):
    """Obtiene detalles de un plan específico."""
    plan = planning_manager.obtener_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    
    return {
        "status": "success",
        "plan": plan.exportar_plan()
    }


@app.put("/planning/plans/{plan_id}/context")
def update_plan_context(plan_id: str, context: Dict[str, Any]):
    """Actualiza el contexto de un plan y ejecuta adaptaciones."""
    plan = planning_manager.obtener_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    
    try:
        contexto = ContextoEjecucion(
            recursos_disponibles=context.get("recursos", []),
            restricciones_tiempo=context.get("tiempo", {}),
            condiciones_externas=context.get("condiciones", {}),
            feedback_usuario=context.get("feedback", []),
            metricas_performance=context.get("metricas", {})
        )
        
        adaptaciones = plan.actualizar_contexto(contexto)
        
        return {
            "status": "success",
            "adaptaciones": adaptaciones,
            "plan_updated": plan.exportar_plan()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando contexto: {str(e)}")


# ============================================================================
# ENDPOINTS DE ESTADO Y SALUD DEL SISTEMA
# ============================================================================

@app.get("/health")
def health_check():
    """Verifica el estado de todos los sistemas."""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "systems": {
            "rag_system": "active",
            "individual_agents": len(agents_cache),
            "multi_agent_crews": len(crews_cache), 
            "active_plans": len(planning_manager.planes_activos)
        },
        "capabilities": [
            "RAG Query (legacy)",
            "Individual Agent with Memory",
            "Multi-Agent Orchestration", 
            "Adaptive Planning",
            "Session Management"
        ]
    }


@app.get("/systems/cleanup")
def cleanup_inactive_sessions():
    """Limpia sesiones inactivas (endpoint de mantenimiento)."""
    # En una implementación real, verificaría timestamps de última actividad
    cleaned_agents = len(agents_cache)
    cleaned_crews = len(crews_cache)
    
    # Reset de caches (simplificado)
    agents_cache.clear()
    crews_cache.clear()
    
    return {
        "status": "success",
        "cleaned": {
            "agent_sessions": cleaned_agents,
            "crew_sessions": cleaned_crews
        }
    }


# ============================================================================
# ENDPOINT DE INFORMACIÓN DEL SISTEMA
# ============================================================================

@app.get("/")
def root():
    """Información general del API."""
    return {
        "name": "CleanPro Intelligent Agent API",
        "version": "2.0.0",
        "description": "Sistema avanzado de agentes inteligentes para automatización organizacional",
        "features": {
            "individual_agents": "Agentes LangChain con memoria conversacional",
            "multi_agent_orchestration": "Crews CrewAI para flujos complejos",
            "adaptive_planning": "Planificación que se adapta a condiciones cambiantes",
            "rag_integration": "Consulta a base de conocimientos organizacional"
        },
        "endpoints": {
            "legacy": "/query - Consulta RAG original",
            "agent": "/agent/query - Agente individual",
            "crew": "/crew/execute - Sistema multi-agente", 
            "planning": "/planning/create - Planificación adaptativa",
            "health": "/health - Estado del sistema"
        }
    }
