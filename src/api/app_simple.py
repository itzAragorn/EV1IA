"""
CleanPro API Simplificada - Totalmente Funcional
================================================
API que integra todos los módulos RA1, RA2 y RA3 sin dependencias complejas.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from datetime import datetime

# Importar módulos RA3
from src.observability.logger_config import setup_logger
from src.observability.metrics_collector import global_metrics
from src.observability.performance_monitor import PerformanceMonitor
from src.traceability.trace_manager import global_trace_manager
from src.traceability.conversation_tracker import global_conversation_tracker
from src.security.input_validator import global_validator
from src.security.ethical_guard import global_ethical_guard
from src.security.rate_limiter import global_rate_limiter
from src.scalability.cache_manager import global_cache_manager
from src.scalability.resource_monitor import global_resource_monitor

# Importar RAG chain
from src.chains.rag_chain import get_rag_chain

load_dotenv()

# Configurar logger
import logging
logger = setup_logger("cleanpro_api", level=logging.INFO)

app = FastAPI(
    title="CleanPro IA API - Completa con RA1, RA2, RA3",
    description="API completa con RAG, Agentes y módulos de Observabilidad, Trazabilidad, Seguridad y Escalabilidad",
    version="3.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sistema RAG
try:
    rag_chain = get_rag_chain()
    logger.info("✅ Sistema RAG inicializado correctamente")
except Exception as e:
    logger.error(f"❌ Error inicializando RAG: {e}")
    rag_chain = None

# ============================================================================
# MODELOS DE DATOS
# ============================================================================

class Query(BaseModel):
    q: str = Field(description="Consulta para el sistema")
    user_id: str = Field(default="anonymous", description="ID del usuario")

class ChatMessage(BaseModel):
    message: str = Field(description="Mensaje del usuario")
    user_id: str = Field(default="anonymous", description="ID del usuario")
    session_id: str = Field(default="default", description="ID de sesión")

class SecurityCheck(BaseModel):
    text: str = Field(description="Texto a validar")

# ============================================================================
# ENDPOINTS RAG (RA1)
# ============================================================================

@app.post("/rag/query")
@PerformanceMonitor.measure_time
def query_rag(body: Query):
    """
    Consulta RAG sobre base de conocimientos.
    Incluye: observabilidad, trazabilidad, seguridad y caché.
    """
    try:
        # Traceability
        trace = global_trace_manager.start_trace("rag_query")
        
        # Metrics
        global_metrics.increment_counter("rag_queries_total")
        
        # Rate Limiting
        if not global_rate_limiter.check_rate_limit(body.user_id, "query"):
            raise HTTPException(status_code=429, detail="Rate limit excedido")
        
        # Input Validation
        is_valid, message = global_validator.validate(body.q)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Input inválido: {message}")
        
        # Ethical check
        is_ethical, ethical_response = global_ethical_guard.validate_and_respond(body.q)
        if not is_ethical:
            return {
                "status": "rejected",
                "reason": "Contenido no ético detectado",
                "ethical_response": ethical_response
            }
        
        # Caché Check
        cache_key = f"rag:{body.q}"
        cached = global_cache_manager.get(cache_key)
        if cached:
            logger.info(f"✅ Cache hit para query: {body.q[:50]}")
            global_metrics.increment_counter("cache_hits")
            return {"answer": cached, "from_cache": True}
        
        # RAG Query
        if not rag_chain:
            raise HTTPException(status_code=503, detail="Sistema RAG no disponible")
        
        result = rag_chain.invoke({"query": body.q})
        answer = result.get("result", "No se encontró respuesta")
        
        # Guardar en caché
        global_cache_manager.set(cache_key, answer, ttl=3600)
        
        # Conversation tracking
        global_conversation_tracker.add_turn(
            user_message=body.q,
            assistant_message=answer,
            tool_used="rag_query"
        )
        
        # End trace
        global_trace_manager.end_trace(trace.trace_id, {"answer_length": len(answer)})
        
        logger.info(f"✅ Query procesada: {body.q[:50]}")
        
        return {
            "answer": answer,
            "from_cache": False,
            "trace_id": trace.trace_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error en query RAG: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS DE CHAT CONVERSACIONAL (RA2)
# ============================================================================

@app.post("/chat")
@PerformanceMonitor.measure_time
def chat_endpoint(body: ChatMessage):
    """
    Endpoint de chat conversacional con memoria.
    Simula un agente conversacional con todos los módulos RA3.
    """
    try:
        # Trace
        trace = global_trace_manager.start_trace("chat")
        
        # Metrics
        global_metrics.increment_counter("chat_messages_total")
        
        # Rate limit
        if not global_rate_limiter.check_rate_limit(body.user_id, "query"):
            raise HTTPException(status_code=429, detail="Rate limit excedido")
        
        # Validación
        is_valid, message = global_validator.validate(body.message)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Input inválido: {message}")
        
        # Ethical check
        is_ethical, ethical_response = global_ethical_guard.validate_and_respond(body.message)
        if not is_ethical:
            response = ethical_response
        else:
            # Procesar con RAG si está disponible
            if rag_chain:
                result = rag_chain.invoke({"query": body.message})
                response = result.get("result", "Procesando tu consulta...")
            else:
                response = f"Recibí tu mensaje: '{body.message}'. Sistema RAG no disponible."
        
        # Track conversation
        global_conversation_tracker.add_turn(
            user_message=body.message,
            assistant_message=response,
            tool_used="chat"
        )
        
        # End trace
        global_trace_manager.end_trace(trace.trace_id, {"response_length": len(response)})
        
        logger.info(f"✅ Chat procesado para user: {body.user_id}")
        
        return {
            "response": response,
            "session_id": body.session_id,
            "trace_id": trace.trace_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error en chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS DE SEGURIDAD (RA3)
# ============================================================================

@app.post("/security/validate")
def validate_input(body: SecurityCheck):
    """Valida input por seguridad."""
    try:
        is_valid, message = global_validator.validate(body.text)
        sanitized = global_validator.sanitize(body.text)
        
        return {
            "is_valid": is_valid,
            "message": message,
            "sanitized": sanitized
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/security/ethical-check")
def ethical_check(body: SecurityCheck):
    """Verifica contenido ético."""
    try:
        is_ethical, response = global_ethical_guard.validate_and_respond(body.text)
        return {
            "is_ethical": is_ethical,
            "ethical_response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS DE OBSERVABILIDAD (RA3)
# ============================================================================

@app.get("/metrics")
def get_metrics():
    """Obtiene métricas del sistema."""
    try:
        return {
            "metrics": global_metrics.get_all_metrics(),
            "cache_stats": global_cache_manager.get_stats(),
            "rate_limiter_stats": global_rate_limiter.get_stats(),
            "system_health": global_resource_monitor.get_system_status()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/traces")
def get_traces():
    """Obtiene todas las trazas."""
    try:
        return {
            "traces": [trace.to_dict() for trace in global_trace_manager.get_all_traces()],
            "active_traces": len(global_trace_manager.active_traces)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversations")
def get_conversations():
    """Obtiene estadísticas de conversaciones."""
    try:
        return global_conversation_tracker.get_conversation_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS DE ESCALABILIDAD (RA3)
# ============================================================================

@app.get("/cache/stats")
def get_cache_stats():
    """Estadísticas de caché."""
    return global_cache_manager.get_stats()


@app.delete("/cache/clear")
def clear_cache():
    """Limpia la caché."""
    global_cache_manager.clear()
    return {"status": "success", "message": "Caché limpiada"}


@app.get("/system/health")
def system_health():
    """Estado de salud del sistema."""
    try:
        health = global_resource_monitor.get_health_status()
        current = global_resource_monitor.get_current_usage()
        return {
            "status": health["status"],
            "cpu_percent": current["cpu_percent"],
            "memory_percent": current["memory_percent"],
            "disk_percent": current["disk_percent"],
            "alerts": health["alerts"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS DE INFORMACIÓN
# ============================================================================

@app.get("/")
def root():
    """Información del API."""
    return {
        "name": "CleanPro IA API Completa",
        "version": "3.0.0",
        "description": "API con integración completa de RA1, RA2 y RA3",
        "modules": {
            "RA1": "Sistema RAG - Consulta base de conocimientos",
            "RA2": "Agentes y Memoria - Conversaciones inteligentes",
            "RA3": {
                "Observabilidad": "Logs, métricas y monitoreo",
                "Trazabilidad": "Tracking de operaciones",
                "Seguridad": "Validación y ética",
                "Escalabilidad": "Caché y recursos"
            }
        },
        "endpoints": {
            "/rag/query": "Consulta RAG",
            "/chat": "Chat conversacional",
            "/security/validate": "Validación de seguridad",
            "/security/ethical-check": "Verificación ética",
            "/metrics": "Métricas del sistema",
            "/traces": "Trazas de operaciones",
            "/conversations": "Estadísticas de conversaciones",
            "/system/health": "Salud del sistema"
        }
    }


@app.get("/health")
def health_check():
    """Health check básico."""
    return {
        "status": "healthy",
        "version": "3.0.0",
        "rag_available": rag_chain is not None,
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Iniciando CleanPro API completa...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
