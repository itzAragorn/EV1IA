"""
IL3.1: Monitor de Rendimiento
Sistema para medir y analizar el rendimiento de operaciones
"""

import time
import functools
from typing import Callable, Any
from contextlib import contextmanager
from .logger_config import get_logger
from .metrics_collector import global_metrics

logger = get_logger(__name__)

class PerformanceMonitor:
    """Monitor de rendimiento para operaciones del sistema"""
    
    @staticmethod
    def measure_time(func: Callable) -> Callable:
        """
        Decorador para medir el tiempo de ejecución de una función
        
        Uso:
            @PerformanceMonitor.measure_time
            def my_function():
                ...
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Registrar métricas
                metric_name = f"function.{func.__name__}.duration"
                global_metrics.record_histogram(metric_name, duration)
                
                # Log
                logger.info(
                    f"⏱️  {func.__name__} ejecutado en {duration:.4f}s",
                    extra={'duration': duration, 'function': func.__name__}
                )
                
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    f"❌ {func.__name__} falló después de {duration:.4f}s: {str(e)}",
                    extra={'duration': duration, 'function': func.__name__, 'error': str(e)}
                )
                raise
        return wrapper
    
    @staticmethod
    @contextmanager
    def measure_block(operation_name: str):
        """
        Context manager para medir bloques de código
        
        Uso:
            with PerformanceMonitor.measure_block("mi_operacion"):
                # código a medir
                ...
        """
        start_time = time.time()
        logger.info(f"🚀 Iniciando: {operation_name}")
        
        try:
            yield
            duration = time.time() - start_time
            
            # Registrar métricas
            global_metrics.record_histogram(f"operation.{operation_name}.duration", duration)
            
            logger.info(
                f"✅ {operation_name} completado en {duration:.4f}s",
                extra={'duration': duration, 'operation': operation_name}
            )
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"❌ {operation_name} falló después de {duration:.4f}s: {str(e)}",
                extra={'duration': duration, 'operation': operation_name, 'error': str(e)}
            )
            raise
    
    @staticmethod
    def log_system_metrics():
        """Registra métricas del sistema actual"""
        import psutil
        
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        global_metrics.set_gauge("system.cpu.percent", cpu_percent)
        global_metrics.set_gauge("system.memory.percent", memory.percent)
        global_metrics.set_gauge("system.memory.available_mb", memory.available / (1024 * 1024))
        
        logger.info(
            f"📊 Sistema - CPU: {cpu_percent}%, Memoria: {memory.percent}%",
            extra={
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_mb': memory.available / (1024 * 1024)
            }
        )
