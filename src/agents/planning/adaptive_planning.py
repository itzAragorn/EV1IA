"""
Sistema de Planificación Adaptativa para Agentes
================================================
Implementa estrategias avanzadas de planificación que se adaptan
a condiciones cambiantes y múltiples etapas de ejecución.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod


class EstadoTarea(Enum):
    """Estados posibles de una tarea."""
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"
    BLOQUEADA = "bloqueada"
    CANCELADA = "cancelada"
    REQUIERE_REVISION = "requiere_revision"


class PrioridadTarea(Enum):
    """Niveles de prioridad de tareas."""
    CRITICA = 1
    ALTA = 2
    MEDIA = 3
    BAJA = 4


@dataclass
class Tarea:
    """Representa una tarea individual en el plan."""
    id: str
    titulo: str
    descripcion: str
    estado: EstadoTarea = EstadoTarea.PENDIENTE
    prioridad: PrioridadTarea = PrioridadTarea.MEDIA
    dependencias: List[str] = None  # IDs de tareas prerequisitos
    recursos_requeridos: List[str] = None
    estimacion_tiempo: int = 60  # minutos
    tiempo_inicio: Optional[datetime] = None
    tiempo_finalizacion: Optional[datetime] = None
    resultado: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.dependencias is None:
            self.dependencias = []
        if self.recursos_requeridos is None:
            self.recursos_requeridos = []
        if self.metadata is None:
            self.metadata = {}


@dataclass  
class ContextoEjecucion:
    """Contexto actual de ejecución del plan."""
    recursos_disponibles: List[str]
    restricciones_tiempo: Dict[str, Any]
    condiciones_externas: Dict[str, Any]
    feedback_usuario: List[str]
    metricas_performance: Dict[str, float]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class EstrategiaAdaptacion(ABC):
    """Interfaz abstracta para estrategias de adaptación."""
    
    @abstractmethod
    def evaluar_necesidad_adaptacion(self, plan: 'PlanAdaptativo', contexto: ContextoEjecucion) -> bool:
        """Evalúa si es necesario adaptar el plan."""
        pass
    
    @abstractmethod
    def adaptar_plan(self, plan: 'PlanAdaptativo', contexto: ContextoEjecucion) -> Dict[str, Any]:
        """Adapta el plan según el contexto."""
        pass


class AdaptacionPorRecursos(EstrategiaAdaptacion):
    """Estrategia de adaptación basada en disponibilidad de recursos."""
    
    def evaluar_necesidad_adaptacion(self, plan: 'PlanAdaptativo', contexto: ContextoEjecucion) -> bool:
        """Evalúa si los recursos disponibles han cambiado significativamente."""
        recursos_actuales = set(contexto.recursos_disponibles)
        recursos_planificados = set(plan.recursos_planificados)
        
        # Evaluar si faltan recursos críticos o hay nuevos recursos disponibles
        recursos_faltantes = recursos_planificados - recursos_actuales
        recursos_nuevos = recursos_actuales - recursos_planificados
        
        return len(recursos_faltantes) > 0 or len(recursos_nuevos) > 0
    
    def adaptar_plan(self, plan: 'PlanAdaptativo', contexto: ContextoEjecucion) -> Dict[str, Any]:
        """Adapta el plan según recursos disponibles."""
        adaptaciones = []
        
        # Identificar tareas afectadas por recursos faltantes
        for tarea in plan.tareas.values():
            if tarea.estado in [EstadoTarea.PENDIENTE, EstadoTarea.EN_PROGRESO]:
                recursos_tarea = set(tarea.recursos_requeridos)
                recursos_disponibles = set(contexto.recursos_disponibles)
                
                if not recursos_tarea.issubset(recursos_disponibles):
                    # Marcar tarea como bloqueada
                    tarea.estado = EstadoTarea.BLOQUEADA
                    adaptaciones.append(f"Tarea {tarea.id} bloqueada por falta de recursos")
                
                elif tarea.estado == EstadoTarea.BLOQUEADA:
                    # Reactivar tarea si ahora hay recursos
                    tarea.estado = EstadoTarea.PENDIENTE
                    adaptaciones.append(f"Tarea {tarea.id} reactivada - recursos disponibles")
        
        return {
            "tipo": "adaptacion_recursos",
            "adaptaciones": adaptaciones,
            "timestamp": datetime.now().isoformat()
        }


class AdaptacionPorTiempo(EstrategiaAdaptacion):
    """Estrategia de adaptación basada en restricciones temporales."""
    
    def evaluar_necesidad_adaptacion(self, plan: 'PlanAdaptativo', contexto: ContextoEjecucion) -> bool:
        """Evalúa si hay presión temporal que requiere adaptación."""
        tiempo_restante = contexto.restricciones_tiempo.get("deadline") 
        if not tiempo_restante:
            return False
        
        # Calcular tiempo estimado para tareas pendientes
        tiempo_estimado = sum(
            tarea.estimacion_tiempo for tarea in plan.tareas.values()
            if tarea.estado == EstadoTarea.PENDIENTE
        )
        
        # Necesita adaptación si el tiempo estimado excede el tiempo disponible
        return tiempo_estimado > tiempo_restante
    
    def adaptar_plan(self, plan: 'PlanAdaptativo', contexto: ContextoEjecucion) -> Dict[str, Any]:
        """Adapta el plan para cumplir restricciones temporales."""
        adaptaciones = []
        
        # Re-priorizar tareas por importancia
        tareas_pendientes = [t for t in plan.tareas.values() if t.estado == EstadoTarea.PENDIENTE]
        tareas_pendientes.sort(key=lambda x: x.prioridad.value)
        
        # Marcar tareas de baja prioridad para cancelación si es necesario
        tiempo_disponible = contexto.restricciones_tiempo.get("deadline", float('inf'))
        tiempo_acumulado = 0
        
        for tarea in tareas_pendientes:
            if tiempo_acumulado + tarea.estimacion_tiempo <= tiempo_disponible:
                tiempo_acumulado += tarea.estimacion_tiempo
            else:
                if tarea.prioridad in [PrioridadTarea.BAJA, PrioridadTarea.MEDIA]:
                    tarea.estado = EstadoTarea.CANCELADA
                    adaptaciones.append(f"Tarea {tarea.id} cancelada por restricciones temporales")
        
        return {
            "tipo": "adaptacion_tiempo",
            "adaptaciones": adaptaciones,
            "tiempo_optimizado": tiempo_acumulado,
            "timestamp": datetime.now().isoformat()
        }


class AdaptacionPorFeedback(EstrategiaAdaptacion):
    """Estrategia de adaptación basada en feedback del usuario."""
    
    def evaluar_necesidad_adaptacion(self, plan: 'PlanAdaptativo', contexto: ContextoEjecucion) -> bool:
        """Evalúa si hay feedback que requiere adaptación."""
        return len(contexto.feedback_usuario) > 0
    
    def adaptar_plan(self, plan: 'PlanAdaptativo', contexto: ContextoEjecucion) -> Dict[str, Any]:
        """Adapta el plan según feedback recibido."""
        adaptaciones = []
        
        for feedback in contexto.feedback_usuario:
            # Análisis simplificado de feedback (en implementación real usaría NLP)
            if "prioridad" in feedback.lower():
                # Re-evaluar prioridades
                adaptaciones.append("Prioridades re-evaluadas según feedback")
            
            elif "cancelar" in feedback.lower():
                # Identificar tareas a cancelar
                adaptaciones.append("Tareas identificadas para cancelación")
            
            elif "nuevo" in feedback.lower() or "agregar" in feedback.lower():
                # Preparar para agregar nuevas tareas
                adaptaciones.append("Nueva tarea identificada para incorporar")
        
        return {
            "tipo": "adaptacion_feedback",
            "adaptaciones": adaptaciones,
            "feedback_procesado": len(contexto.feedback_usuario),
            "timestamp": datetime.now().isoformat()
        }


class PlanAdaptativo:
    """
    Sistema de planificación adaptativa que ajusta estrategias
    según condiciones cambiantes y múltiples etapas.
    """
    
    def __init__(self, plan_id: str, objetivo: str):
        self.plan_id = plan_id
        self.objetivo = objetivo
        self.tareas: Dict[str, Tarea] = {}
        self.recursos_planificados: List[str] = []
        self.estrategias_adaptacion: List[EstrategiaAdaptacion] = []
        self.historial_adaptaciones: List[Dict[str, Any]] = []
        self.contexto_actual: Optional[ContextoEjecucion] = None
        self.metricas: Dict[str, Any] = {}
        
        # Configurar estrategias por defecto
        self._setup_estrategias_default()
        
        # Metadatos del plan
        self.metadata = {
            "creado": datetime.now().isoformat(),
            "ultima_adaptacion": None,
            "version": "1.0",
            "status": "activo"
        }
    
    def _setup_estrategias_default(self):
        """Configura estrategias de adaptación por defecto."""
        self.estrategias_adaptacion = [
            AdaptacionPorRecursos(),
            AdaptacionPorTiempo(),
            AdaptacionPorFeedback()
        ]
    
    def agregar_tarea(self, tarea: Tarea):
        """Agrega una tarea al plan."""
        self.tareas[tarea.id] = tarea
        
        # Actualizar recursos planificados
        for recurso in tarea.recursos_requeridos:
            if recurso not in self.recursos_planificados:
                self.recursos_planificados.append(recurso)
    
    def actualizar_contexto(self, contexto: ContextoEjecucion):
        """Actualiza el contexto de ejecución y evalúa necesidad de adaptación."""
        self.contexto_actual = contexto
        
        # Evaluar cada estrategia de adaptación
        adaptaciones_realizadas = []
        
        for estrategia in self.estrategias_adaptacion:
            if estrategia.evaluar_necesidad_adaptacion(self, contexto):
                adaptacion = estrategia.adaptar_plan(self, contexto)
                adaptaciones_realizadas.append(adaptacion)
                self.historial_adaptaciones.append(adaptacion)
        
        if adaptaciones_realizadas:
            self.metadata["ultima_adaptacion"] = datetime.now().isoformat()
            self._actualizar_metricas()
        
        return adaptaciones_realizadas
    
    def ejecutar_siguiente_tarea(self) -> Optional[Tarea]:
        """Identifica y retorna la siguiente tarea a ejecutar."""
        # Obtener tareas ejecutables (sin dependencias bloqueadas)
        tareas_ejecutables = []
        
        for tarea in self.tareas.values():
            if tarea.estado == EstadoTarea.PENDIENTE:
                # Verificar dependencias
                dependencias_completas = all(
                    self.tareas[dep_id].estado == EstadoTarea.COMPLETADA
                    for dep_id in tarea.dependencias
                    if dep_id in self.tareas
                )
                
                if dependencias_completas:
                    tareas_ejecutables.append(tarea)
        
        if not tareas_ejecutables:
            return None
        
        # Ordenar por prioridad y seleccionar la primera
        tareas_ejecutables.sort(key=lambda x: x.prioridad.value)
        tarea_siguiente = tareas_ejecutables[0]
        
        # Marcar como en progreso
        tarea_siguiente.estado = EstadoTarea.EN_PROGRESO
        tarea_siguiente.tiempo_inicio = datetime.now()
        
        return tarea_siguiente
    
    def completar_tarea(self, tarea_id: str, resultado: str = None):
        """Marca una tarea como completada."""
        if tarea_id in self.tareas:
            tarea = self.tareas[tarea_id]
            tarea.estado = EstadoTarea.COMPLETADA
            tarea.tiempo_finalizacion = datetime.now()
            tarea.resultado = resultado
            
            self._actualizar_metricas()
    
    def obtener_progreso(self) -> Dict[str, Any]:
        """Obtiene información sobre el progreso del plan."""
        total_tareas = len(self.tareas)
        if total_tareas == 0:
            return {"progreso": 0, "completadas": 0, "total": 0}
        
        tareas_completadas = sum(1 for t in self.tareas.values() if t.estado == EstadoTarea.COMPLETADA)
        tareas_en_progreso = sum(1 for t in self.tareas.values() if t.estado == EstadoTarea.EN_PROGRESO)
        tareas_bloqueadas = sum(1 for t in self.tareas.values() if t.estado == EstadoTarea.BLOQUEADA)
        
        progreso_porcentaje = (tareas_completadas / total_tareas) * 100
        
        return {
            "progreso": round(progreso_porcentaje, 2),
            "completadas": tareas_completadas,
            "en_progreso": tareas_en_progreso,
            "bloqueadas": tareas_bloqueadas,
            "total": total_tareas,
            "adaptaciones_realizadas": len(self.historial_adaptaciones)
        }
    
    def _actualizar_metricas(self):
        """Actualiza métricas del plan."""
        progreso = self.obtener_progreso()
        
        # Calcular tiempo promedio por tarea
        tareas_completadas = [t for t in self.tareas.values() if t.estado == EstadoTarea.COMPLETADA]
        if tareas_completadas:
            tiempos_ejecucion = []
            for tarea in tareas_completadas:
                if tarea.tiempo_inicio and tarea.tiempo_finalizacion:
                    tiempo_ejecucion = (tarea.tiempo_finalizacion - tarea.tiempo_inicio).total_seconds() / 60
                    tiempos_ejecucion.append(tiempo_ejecucion)
            
            if tiempos_ejecucion:
                self.metricas["tiempo_promedio_tarea"] = sum(tiempos_ejecucion) / len(tiempos_ejecucion)
        
        # Actualizar métricas generales
        self.metricas.update({
            "progreso_actual": progreso["progreso"],
            "eficacia_adaptacion": len(self.historial_adaptaciones),
            "ultima_actualizacion": datetime.now().isoformat()
        })
    
    def exportar_plan(self) -> Dict[str, Any]:
        """Exporta el plan completo a formato JSON serializable."""
        return {
            "plan_id": self.plan_id,
            "objetivo": self.objetivo,
            "tareas": {tid: asdict(tarea) for tid, tarea in self.tareas.items()},
            "recursos_planificados": self.recursos_planificados,
            "historial_adaptaciones": self.historial_adaptaciones,
            "metricas": self.metricas,
            "metadata": self.metadata,
            "progreso": self.obtener_progreso()
        }
    
    def guardar_plan(self, directorio: str = "plans"):
        """Guarda el plan en disco."""
        os.makedirs(directorio, exist_ok=True)
        filepath = os.path.join(directorio, f"{self.plan_id}.json")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.exportar_plan(), f, indent=2, ensure_ascii=False, default=str)
        
        return filepath


class GestorPlanificacionAdaptativa:
    """Gestor central para múltiples planes adaptativos."""
    
    def __init__(self):
        self.planes_activos: Dict[str, PlanAdaptativo] = {}
        self.historial_planes: List[str] = []
    
    def crear_plan(self, plan_id: str, objetivo: str) -> PlanAdaptativo:
        """Crea un nuevo plan adaptativo."""
        plan = PlanAdaptativo(plan_id, objetivo)
        self.planes_activos[plan_id] = plan
        return plan
    
    def obtener_plan(self, plan_id: str) -> Optional[PlanAdaptativo]:
        """Obtiene un plan existente."""
        return self.planes_activos.get(plan_id)
    
    def listar_planes(self) -> List[Dict[str, Any]]:
        """Lista todos los planes activos."""
        return [
            {
                "plan_id": plan.plan_id,
                "objetivo": plan.objetivo,
                "progreso": plan.obtener_progreso(),
                "status": plan.metadata["status"]
            }
            for plan in self.planes_activos.values()
        ]
    
    def finalizar_plan(self, plan_id: str):
        """Finaliza un plan y lo mueve al historial."""
        if plan_id in self.planes_activos:
            plan = self.planes_activos[plan_id]
            plan.metadata["status"] = "finalizado"
            plan.guardar_plan()
            
            self.historial_planes.append(plan_id)
            del self.planes_activos[plan_id]


# Instancia global del gestor
planning_manager = GestorPlanificacionAdaptativa()