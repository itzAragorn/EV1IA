"""
IL3.4: Monitor de Recursos
Sistema para monitorear recursos del sistema
"""

import psutil
import time
from typing import Dict, List
from dataclasses import dataclass
from ..observability.logger_config import get_logger
from ..observability.metrics_collector import global_metrics

logger = get_logger(__name__)

@dataclass
class ResourceSnapshot:
    """Snapshot de recursos del sistema"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_available_mb: float
    memory_used_mb: float
    disk_percent: float
    network_sent_mb: float
    network_recv_mb: float
    
    def to_dict(self) -> dict:
        return {
            'timestamp': self.timestamp,
            'cpu_percent': self.cpu_percent,
            'memory_percent': self.memory_percent,
            'memory_available_mb': self.memory_available_mb,
            'memory_used_mb': self.memory_used_mb,
            'disk_percent': self.disk_percent,
            'network_sent_mb': self.network_sent_mb,
            'network_recv_mb': self.network_recv_mb
        }

class ResourceMonitor:
    """
    Monitor de recursos del sistema
    Implementa IL3.4: Escalabilidad y Sostenibilidad
    """
    
    def __init__(self, alert_cpu_threshold: float = 80.0, alert_memory_threshold: float = 85.0):
        self.alert_cpu_threshold = alert_cpu_threshold
        self.alert_memory_threshold = alert_memory_threshold
        self.snapshots: List[ResourceSnapshot] = []
        self.alerts: List[Dict] = []
        
    def take_snapshot(self) -> ResourceSnapshot:
        """Toma un snapshot de los recursos actuales"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        snapshot = ResourceSnapshot(
            timestamp=time.time(),
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_available_mb=memory.available / (1024 * 1024),
            memory_used_mb=memory.used / (1024 * 1024),
            disk_percent=disk.percent,
            network_sent_mb=network.bytes_sent / (1024 * 1024),
            network_recv_mb=network.bytes_recv / (1024 * 1024)
        )
        
        self.snapshots.append(snapshot)
        
        # Registrar métricas
        global_metrics.set_gauge('system.cpu.percent', cpu_percent)
        global_metrics.set_gauge('system.memory.percent', memory.percent)
        global_metrics.set_gauge('system.memory.available_mb', snapshot.memory_available_mb)
        global_metrics.set_gauge('system.disk.percent', disk.percent)
        
        # Verificar alertas
        self._check_alerts(snapshot)
        
        return snapshot
    
    def _check_alerts(self, snapshot: ResourceSnapshot):
        """Verifica si se deben generar alertas"""
        if snapshot.cpu_percent > self.alert_cpu_threshold:
            alert = {
                'type': 'cpu',
                'timestamp': snapshot.timestamp,
                'value': snapshot.cpu_percent,
                'threshold': self.alert_cpu_threshold,
                'message': f"CPU usage high: {snapshot.cpu_percent:.1f}%"
            }
            self.alerts.append(alert)
            logger.warning(f"⚠️  {alert['message']}")
        
        if snapshot.memory_percent > self.alert_memory_threshold:
            alert = {
                'type': 'memory',
                'timestamp': snapshot.timestamp,
                'value': snapshot.memory_percent,
                'threshold': self.alert_memory_threshold,
                'message': f"Memory usage high: {snapshot.memory_percent:.1f}%"
            }
            self.alerts.append(alert)
            logger.warning(f"⚠️  {alert['message']}")
    
    def get_current_usage(self) -> Dict:
        """Obtiene el uso actual de recursos"""
        if not self.snapshots:
            self.take_snapshot()
        
        latest = self.snapshots[-1]
        return latest.to_dict()
    
    def get_average_usage(self, last_n: int = 10) -> Dict:
        """Calcula el promedio de uso de recursos"""
        if not self.snapshots:
            return {}
        
        recent_snapshots = self.snapshots[-last_n:]
        
        return {
            'cpu_percent_avg': sum(s.cpu_percent for s in recent_snapshots) / len(recent_snapshots),
            'memory_percent_avg': sum(s.memory_percent for s in recent_snapshots) / len(recent_snapshots),
            'disk_percent_avg': sum(s.disk_percent for s in recent_snapshots) / len(recent_snapshots)
        }
    
    def get_peak_usage(self) -> Dict:
        """Obtiene el uso máximo registrado"""
        if not self.snapshots:
            return {}
        
        return {
            'cpu_percent_max': max(s.cpu_percent for s in self.snapshots),
            'memory_percent_max': max(s.memory_percent for s in self.snapshots),
            'disk_percent_max': max(s.disk_percent for s in self.snapshots)
        }
    
    def get_health_status(self) -> Dict:
        """Evalúa el estado de salud del sistema"""
        current = self.get_current_usage()
        
        status = 'healthy'
        issues = []
        
        if current['cpu_percent'] > self.alert_cpu_threshold:
            status = 'warning'
            issues.append(f"High CPU usage: {current['cpu_percent']:.1f}%")
        
        if current['memory_percent'] > self.alert_memory_threshold:
            status = 'critical' if current['memory_percent'] > 95 else 'warning'
            issues.append(f"High memory usage: {current['memory_percent']:.1f}%")
        
        if current['disk_percent'] > 90:
            status = 'critical'
            issues.append(f"High disk usage: {current['disk_percent']:.1f}%")
        
        return {
            'status': status,
            'issues': issues,
            'current_usage': current,
            'total_alerts': len(self.alerts)
        }
    
    def get_recommendations(self) -> List[str]:
        """Obtiene recomendaciones de optimización"""
        recommendations = []
        current = self.get_current_usage()
        
        if current['cpu_percent'] > 70:
            recommendations.append("Considere escalar horizontalmente o optimizar procesos CPU-intensivos")
        
        if current['memory_percent'] > 80:
            recommendations.append("Considere aumentar memoria RAM o implementar caché más agresivo")
            recommendations.append("Revise posibles memory leaks en la aplicación")
        
        if current['disk_percent'] > 85:
            recommendations.append("Considere expandir almacenamiento o limpiar archivos temporales")
            recommendations.append("Implemente rotación de logs automática")
        
        if len(self.snapshots) > 100:
            avg = self.get_average_usage()
            if avg['cpu_percent_avg'] > 60:
                recommendations.append("Uso promedio de CPU alto - considere load balancing")
        
        return recommendations
    
    def print_status(self):
        """Imprime el estado actual del sistema"""
        health = self.get_health_status()
        current = health['current_usage']
        
        print("\n" + "=" * 60)
        print("🖥️  ESTADO DEL SISTEMA")
        print("=" * 60)
        print(f"Estado: {health['status'].upper()}")
        print(f"\n📊 Recursos Actuales:")
        print(f"  CPU: {current['cpu_percent']:.1f}%")
        print(f"  Memoria: {current['memory_percent']:.1f}% ({current['memory_used_mb']:.0f}MB usado)")
        print(f"  Disco: {current['disk_percent']:.1f}%")
        
        if health['issues']:
            print(f"\n⚠️  Problemas detectados:")
            for issue in health['issues']:
                print(f"  - {issue}")
        
        recommendations = self.get_recommendations()
        if recommendations:
            print(f"\n💡 Recomendaciones:")
            for rec in recommendations:
                print(f"  - {rec}")
        
        print("=" * 60 + "\n")

# Instancia global del monitor
global_resource_monitor = ResourceMonitor()
