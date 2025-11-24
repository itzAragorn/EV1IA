"""
IL3.2: Gestor de Trazas
Sistema para rastrear y analizar el flujo de ejecución
"""

import uuid
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path
from ..observability.logger_config import get_logger

logger = get_logger(__name__)

@dataclass
class TraceSpan:
    """Representa un segmento de una traza"""
    span_id: str
    name: str
    start_time: float
    end_time: Optional[float] = None
    tags: Dict[str, Any] = field(default_factory=dict)
    logs: List[Dict[str, Any]] = field(default_factory=list)
    parent_span_id: Optional[str] = None
    
    @property
    def duration(self) -> Optional[float]:
        """Duración del span en segundos"""
        if self.end_time:
            return self.end_time - self.start_time
        return None
    
    def to_dict(self) -> dict:
        return {
            'span_id': self.span_id,
            'name': self.name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'tags': self.tags,
            'logs': self.logs,
            'parent_span_id': self.parent_span_id
        }

@dataclass
class Trace:
    """Representa una traza completa de ejecución"""
    trace_id: str
    operation: str
    start_time: float
    end_time: Optional[float] = None
    spans: List[TraceSpan] = field(default_factory=list)
    tags: Dict[str, Any] = field(default_factory=dict)
    status: str = "running"  # running, success, error
    error: Optional[str] = None
    
    @property
    def duration(self) -> Optional[float]:
        """Duración total de la traza"""
        if self.end_time:
            return self.end_time - self.start_time
        return None
    
    def to_dict(self) -> dict:
        return {
            'trace_id': self.trace_id,
            'operation': self.operation,
            'start_time': self.start_time,
            'start_datetime': datetime.fromtimestamp(self.start_time).isoformat(),
            'end_time': self.end_time,
            'end_datetime': datetime.fromtimestamp(self.end_time).isoformat() if self.end_time else None,
            'duration': self.duration,
            'status': self.status,
            'error': self.error,
            'tags': self.tags,
            'spans': [span.to_dict() for span in self.spans]
        }

class TraceManager:
    """
    Gestor de trazas para análisis de trazabilidad
    Implementa IL3.2: Análisis de Trazabilidad y Logs
    """
    
    def __init__(self):
        self.active_traces: Dict[str, Trace] = {}
        self.completed_traces: List[Trace] = []
        self.active_spans: Dict[str, TraceSpan] = {}
        
    def start_trace(self, operation: str, **tags) -> str:
        """Inicia una nueva traza"""
        trace_id = str(uuid.uuid4())
        trace = Trace(
            trace_id=trace_id,
            operation=operation,
            start_time=time.time(),
            tags=tags
        )
        self.active_traces[trace_id] = trace
        
        logger.info(f"🔍 Iniciando traza: {operation} [{trace_id}]", extra={'trace_id': trace_id})
        return trace_id
    
    def end_trace(self, trace_id: str, status: str = "success", error: Optional[str] = None):
        """Finaliza una traza"""
        if trace_id not in self.active_traces:
            logger.warning(f"Traza no encontrada: {trace_id}")
            return
            
        trace = self.active_traces[trace_id]
        trace.end_time = time.time()
        trace.status = status
        trace.error = error
        
        self.completed_traces.append(trace)
        del self.active_traces[trace_id]
        
        logger.info(
            f"✅ Traza completada: {trace.operation} [{trace_id}] - {trace.duration:.4f}s - {status}",
            extra={'trace_id': trace_id, 'duration': trace.duration, 'status': status}
        )
    
    def start_span(self, trace_id: str, name: str, parent_span_id: Optional[str] = None, **tags) -> str:
        """Inicia un nuevo span dentro de una traza"""
        if trace_id not in self.active_traces:
            logger.warning(f"Traza no encontrada: {trace_id}")
            return ""
            
        span_id = str(uuid.uuid4())
        span = TraceSpan(
            span_id=span_id,
            name=name,
            start_time=time.time(),
            parent_span_id=parent_span_id,
            tags=tags
        )
        
        self.active_spans[span_id] = span
        self.active_traces[trace_id].spans.append(span)
        
        logger.debug(f"  📍 Span iniciado: {name} [{span_id}]")
        return span_id
    
    def end_span(self, span_id: str, **tags):
        """Finaliza un span"""
        if span_id not in self.active_spans:
            logger.warning(f"Span no encontrado: {span_id}")
            return
            
        span = self.active_spans[span_id]
        span.end_time = time.time()
        span.tags.update(tags)
        
        del self.active_spans[span_id]
        
        logger.debug(f"  ✓ Span completado: {span.name} - {span.duration:.4f}s")
    
    def add_span_log(self, span_id: str, message: str, **data):
        """Agrega un log a un span"""
        if span_id in self.active_spans:
            span = self.active_spans[span_id]
            span.logs.append({
                'timestamp': time.time(),
                'message': message,
                **data
            })
    
    def get_trace(self, trace_id: str) -> Optional[Trace]:
        """Obtiene una traza por ID"""
        if trace_id in self.active_traces:
            return self.active_traces[trace_id]
        
        for trace in self.completed_traces:
            if trace.trace_id == trace_id:
                return trace
        return None
    
    def get_all_traces(self) -> List[Trace]:
        """Obtiene todas las trazas (activas y completadas)"""
        return list(self.active_traces.values()) + self.completed_traces
    
    def get_traces_summary(self) -> Dict:
        """Genera un resumen de todas las trazas"""
        all_traces = self.get_all_traces()
        
        successful = [t for t in all_traces if t.status == "success"]
        failed = [t for t in all_traces if t.status == "error"]
        running = [t for t in all_traces if t.status == "running"]
        
        completed_durations = [t.duration for t in successful + failed if t.duration]
        
        return {
            'total_traces': len(all_traces),
            'active': len(running),
            'successful': len(successful),
            'failed': len(failed),
            'avg_duration': sum(completed_durations) / len(completed_durations) if completed_durations else 0,
            'total_duration': sum(completed_durations) if completed_durations else 0
        }
    
    def save_traces(self, filepath: str, include_active: bool = False):
        """Guarda las trazas a un archivo JSON"""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        traces_to_save = self.completed_traces
        if include_active:
            traces_to_save = traces_to_save + list(self.active_traces.values())
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'summary': self.get_traces_summary(),
            'traces': [trace.to_dict() for trace in traces_to_save]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Trazas guardadas en: {filepath}")

# Instancia global del gestor de trazas
global_trace_manager = TraceManager()
