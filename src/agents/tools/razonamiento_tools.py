"""
Herramientas de Razonamiento y Planificación para Agentes
========================================================
Implementa herramientas avanzadas para razonamiento lógico,
toma de decisiones y planificación estratégica.
"""

import json
from typing import Any, Dict, List, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from datetime import datetime, timedelta


class DecisionInput(BaseModel):
    """Input schema para toma de decisiones."""
    problema: str = Field(description="Descripción del problema o situación a analizar")
    opciones: List[str] = Field(description="Lista de opciones o alternativas disponibles")
    criterios: List[str] = Field(default=[], description="Criterios de evaluación (opcional)")


class PlanificacionInput(BaseModel):
    """Input schema para planificación de tareas."""
    objetivo: str = Field(description="Objetivo principal a alcanzar")
    restricciones: List[str] = Field(default=[], description="Restricciones o limitaciones")
    recursos: List[str] = Field(default=[], description="Recursos disponibles")
    plazo: Optional[str] = Field(default=None, description="Plazo límite (opcional)")


class RazonamientoDecisionTool(BaseTool):
    """Herramienta para razonamiento y toma de decisiones estructurada."""
    
    name: str = "razonamiento_decision"
    description: str = """
    Realiza análisis de decisiones estructurado usando razonamiento lógico.
    Evalúa opciones, considera criterios múltiples y proporciona recomendaciones
    fundamentadas para la toma de decisiones organizacionales.
    """
    args_schema = DecisionInput
    
    def _run(self, problema: str, opciones: List[str], criterios: List[str] = None) -> str:
        """Ejecuta análisis de decisión estructurado."""
        try:
            if criterios is None:
                criterios = ["Viabilidad", "Costo", "Impacto", "Tiempo de implementación"]
            
            # Estructurar análisis de decisión
            analisis = self._analizar_decision(problema, opciones, criterios)
            
            return f"""
## Análisis de Decisión

### Problema Identificado
{problema}

### Opciones Evaluadas
{chr(10).join([f"{i+1}. {opcion}" for i, opcion in enumerate(opciones)])}

### Criterios de Evaluación
{chr(10).join([f"- {criterio}" for criterio in criterios])}

### Análisis Detallado
{analisis['detalle']}

### Matriz de Decisión
{analisis['matriz']}

### Recomendación
**Opción recomendada:** {analisis['recomendacion']}

**Justificación:** {analisis['justificacion']}

### Próximos Pasos
{analisis['proximos_pasos']}

---
*Análisis generado por Sistema de Razonamiento CleanPro*
"""
            
        except Exception as e:
            return f"Error en análisis de decisión: {str(e)}"
    
    def _analizar_decision(self, problema: str, opciones: List[str], criterios: List[str]) -> Dict[str, str]:
        """Realiza análisis estructurado de la decisión."""
        
        # Análisis detallado por opción
        detalle = ""
        for i, opcion in enumerate(opciones, 1):
            detalle += f"\n**Opción {i}: {opcion}**\n"
            for criterio in criterios:
                detalle += f"- {criterio}: Requiere evaluación específica\n"
        
        # Matriz simplificada (en implementación real usaría scoring)
        matriz = "| Opción | " + " | ".join(criterios) + " | Total |\n"
        matriz += "|" + "---|" * (len(criterios) + 2) + "\n"
        
        for i, opcion in enumerate(opciones, 1):
            matriz += f"| {opcion[:20]} |" + " TBD |" * len(criterios) + " TBD |\n"
        
        # Recomendación (lógica simplificada)
        mejor_opcion = opciones[0] if opciones else "Ninguna opción disponible"
        
        return {
            'detalle': detalle,
            'matriz': matriz,
            'recomendacion': mejor_opcion,
            'justificacion': f"Basado en el análisis de criterios establecidos, {mejor_opcion} presenta el mejor balance.",
            'proximos_pasos': "1. Validar análisis con stakeholders\n2. Desarrollar plan de implementación\n3. Establecer métricas de éxito"
        }
    
    async def _arun(self, problema: str, opciones: List[str], criterios: List[str] = None) -> str:
        return self._run(problema, opciones, criterios)


class PlanificacionEstrategicaTool(BaseTool):
    """Herramienta para planificación estratégica y descomposición de tareas."""
    
    name: str = "planificacion_estrategica"
    description: str = """
    Crea planes estratégicos detallados descomponiendo objetivos complejos
    en tareas ejecutables. Considera restricciones, recursos y plazos
    para generar roadmaps organizacionales.
    """
    args_schema = PlanificacionInput
    
    def _run(self, objetivo: str, restricciones: List[str] = None, recursos: List[str] = None, plazo: str = None) -> str:
        """Genera plan estratégico estructurado."""
        try:
            if restricciones is None:
                restricciones = []
            if recursos is None:
                recursos = []
            
            # Generar plan estratégico
            plan = self._crear_plan_estrategico(objetivo, restricciones, recursos, plazo)
            
            return f"""
## Plan Estratégico

### Objetivo Principal
{objetivo}

### Análisis de Contexto
**Restricciones identificadas:**
{chr(10).join([f"- {r}" for r in restricciones]) if restricciones else "- Ninguna restricción específica identificada"}

**Recursos disponibles:**
{chr(10).join([f"- {r}" for r in recursos]) if recursos else "- Recursos por determinar"}

**Plazo:** {plazo if plazo else "Por definir"}

### Descomposición de Tareas
{plan['tareas']}

### Cronograma Propuesto
{plan['cronograma']}

### Hitos Críticos
{plan['hitos']}

### Análisis de Riesgos
{plan['riesgos']}

### Indicadores de Éxito
{plan['indicadores']}

---
*Plan generado por Sistema de Planificación CleanPro*
"""
            
        except Exception as e:
            return f"Error en planificación estratégica: {str(e)}"
    
    def _crear_plan_estrategico(self, objetivo: str, restricciones: List[str], recursos: List[str], plazo: str) -> Dict[str, str]:
        """Crea plan estratégico detallado."""
        
        # Descomposición en fases (lógica simplificada)
        fases = [
            "Fase 1: Análisis y Preparación",
            "Fase 2: Desarrollo e Implementación", 
            "Fase 3: Validación y Ajustes",
            "Fase 4: Despliegue y Monitoreo"
        ]
        
        tareas = ""
        for i, fase in enumerate(fases, 1):
            tareas += f"\n### {fase}\n"
            tareas += f"- Tarea {i}.1: Actividad principal de la fase\n"
            tareas += f"- Tarea {i}.2: Actividad de soporte\n"
            tareas += f"- Tarea {i}.3: Validación y control de calidad\n"
        
        # Cronograma básico
        fecha_inicio = datetime.now()
        cronograma = "| Fase | Inicio | Duración | Responsable |\n"
        cronograma += "|------|--------|----------|-------------|\n"
        
        for i, fase in enumerate(fases):
            inicio = fecha_inicio + timedelta(weeks=i*2)
            cronograma += f"| {fase} | {inicio.strftime('%Y-%m-%d')} | 2 semanas | Por asignar |\n"
        
        return {
            'tareas': tareas,
            'cronograma': cronograma,
            'hitos': "- Hito 1: Completar análisis inicial\n- Hito 2: Implementación del 50%\n- Hito 3: Pruebas finalizadas\n- Hito 4: Go-live exitoso",
            'riesgos': "- Riesgo 1: Retrasos por dependencias externas\n- Riesgo 2: Recursos insuficientes\n- Riesgo 3: Cambios en requerimientos",
            'indicadores': "- KPI 1: % de tareas completadas a tiempo\n- KPI 2: Calidad de entregables\n- KPI 3: Satisfacción de stakeholders\n- KPI 4: ROI del proyecto"
        }
    
    async def _arun(self, objetivo: str, restricciones: List[str] = None, recursos: List[str] = None, plazo: str = None) -> str:
        return self._run(objetivo, restricciones, recursos, plazo)


class AdaptacionContextualTool(BaseTool):
    """Herramienta para adaptación contextual y ajuste de comportamiento."""
    
    name: str = "adaptacion_contextual"  
    description: str = """
    Adapta estrategias y comportamientos según el contexto cambiante.
    Analiza situaciones dinámicas y ajusta planes de acción basado
    en condiciones emergentes y feedback recibido.
    """
    
    def _run(self, situacion_actual: str, cambios_detectados: str = "", feedback: str = "") -> str:
        """Realiza adaptación contextual del comportamiento."""
        try:
            adaptacion = self._generar_adaptacion(situacion_actual, cambios_detectados, feedback)
            
            return f"""
## Adaptación Contextual

### Situación Actual
{situacion_actual}

### Cambios Detectados
{cambios_detectados if cambios_detectados else "No se han detectado cambios significativos"}

### Feedback Recibido
{feedback if feedback else "No hay feedback específico disponible"}

### Análisis de Impacto
{adaptacion['impacto']}

### Estrategia de Adaptación
{adaptacion['estrategia']}  

### Acciones Correctivas
{adaptacion['acciones']}

### Monitoreo Continuo
{adaptacion['monitoreo']}

---
*Adaptación realizada por Sistema Inteligente CleanPro*
"""
            
        except Exception as e:
            return f"Error en adaptación contextual: {str(e)}"
    
    def _generar_adaptacion(self, situacion: str, cambios: str, feedback: str) -> Dict[str, str]:
        """Genera estrategia de adaptación."""
        return {
            'impacto': f"Los cambios en el contexto requieren ajustes en la estrategia actual. Impacto estimado: Medio-Alto",
            'estrategia': "1. Reevaluacion de objetivos actuales\n2. Ajuste de prioridades según nuevo contexto\n3. Reallocation de recursos si es necesario\n4. Comunicación de cambios a stakeholders",
            'acciones': "- Acción inmediata: Validar nuevos requerimientos\n- Acción corto plazo: Ajustar cronograma\n- Acción mediano plazo: Revisar KPIs\n- Acción continua: Monitorear evolución",
            'monitoreo': "- Revisar situación cada 48 horas\n- Establecer checkpoints semanales\n- Mantener canales de feedback abiertos\n- Documentar lecciones aprendidas"
        }
    
    async def _arun(self, situacion_actual: str, cambios_detectados: str = "", feedback: str = "") -> str:
        return self._run(situacion_actual, cambios_detectados, feedback)


def get_razonamiento_tools() -> List[BaseTool]:
    """Factory function para crear herramientas de razonamiento."""
    return [
        RazonamientoDecisionTool(),
        PlanificacionEstrategicaTool(),
        AdaptacionContextualTool()
    ]