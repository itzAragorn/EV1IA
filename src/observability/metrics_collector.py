"""
IL3.1: Colector de Métricas
Sistema para recolectar y analizar métricas de desempeño
"""

import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path
from collections import defaultdict

@dataclass
class Metric:
    """Representa una métrica individual"""
    name: str
    value: float
    timestamp: float = field(default_factory=time.time)
    tags: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'value': self.value,
            'timestamp': self.timestamp,
            'datetime': datetime.fromtimestamp(self.timestamp).isoformat(),
            'tags': self.tags
        }

class MetricsCollector:
    """
    Colector centralizado de métricas del sistema
    Implementa IL3.1: Observabilidad y Métricas
    """
    
    def __init__(self):
        self.metrics: List[Metric] = []
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = defaultdict(list)
        
    def increment_counter(self, name: str, value: int = 1, **tags):
        """Incrementa un contador"""
        self.counters[name] += value
        self.record_metric(name, self.counters[name], **tags)
        
    def set_gauge(self, name: str, value: float, **tags):
        """Establece un valor gauge (medición instantánea)"""
        self.gauges[name] = value
        self.record_metric(name, value, **tags)
        
    def record_histogram(self, name: str, value: float, **tags):
        """Registra un valor en un histograma"""
        self.histograms[name].append(value)
        self.record_metric(name, value, **tags)
        
    def record_metric(self, name: str, value: float, **tags):
        """Registra una métrica genérica"""
        metric = Metric(name=name, value=value, tags=tags)
        self.metrics.append(metric)
        
    def get_counter(self, name: str) -> int:
        """Obtiene el valor actual de un contador"""
        return self.counters.get(name, 0)
    
    def get_gauge(self, name: str) -> Optional[float]:
        """Obtiene el valor actual de un gauge"""
        return self.gauges.get(name)
    
    def get_histogram_stats(self, name: str) -> Dict[str, float]:
        """Calcula estadísticas de un histograma"""
        values = self.histograms.get(name, [])
        if not values:
            return {}
            
        return {
            'count': len(values),
            'min': min(values),
            'max': max(values),
            'avg': sum(values) / len(values),
            'sum': sum(values)
        }
    
    def get_all_metrics(self) -> List[Dict]:
        """Obtiene todas las métricas registradas"""
        return [m.to_dict() for m in self.metrics]
    
    def get_summary(self) -> Dict:
        """Genera un resumen de todas las métricas"""
        return {
            'total_metrics': len(self.metrics),
            'counters': dict(self.counters),
            'gauges': dict(self.gauges),
            'histograms': {
                name: self.get_histogram_stats(name)
                for name in self.histograms.keys()
            }
        }
    
    def save_to_file(self, filepath: str):
        """Guarda métricas a un archivo JSON"""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'summary': self.get_summary(),
            'metrics': self.get_all_metrics()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def clear(self):
        """Limpia todas las métricas"""
        self.metrics.clear()
        self.counters.clear()
        self.gauges.clear()
        self.histograms.clear()

# Instancia global del colector
global_metrics = MetricsCollector()
