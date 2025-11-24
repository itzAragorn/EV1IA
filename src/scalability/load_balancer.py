"""
IL3.4: Balanceador de Carga
Sistema simple de balanceo de carga para distribuir trabajo
"""

import time
from typing import List, Callable, Any, Dict
from dataclasses import dataclass
from enum import Enum
from ..observability.logger_config import get_logger

logger = get_logger(__name__)

class LoadBalancingStrategy(Enum):
    """Estrategias de balanceo de carga"""
    ROUND_ROBIN = "round_robin"
    LEAST_LOADED = "least_loaded"
    RANDOM = "random"

@dataclass
class Worker:
    """Representa un worker que puede procesar tareas"""
    id: str
    handler: Callable
    current_load: int = 0
    total_processed: int = 0
    total_errors: int = 0
    avg_processing_time: float = 0.0
    
class LoadBalancer:
    """
    Balanceador de carga para distribuir trabajo
    Implementa IL3.4: Escalabilidad
    """
    
    def __init__(self, strategy: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN):
        self.strategy = strategy
        self.workers: List[Worker] = []
        self.current_index = 0
        
    def add_worker(self, worker_id: str, handler: Callable):
        """Agrega un worker al pool"""
        worker = Worker(id=worker_id, handler=handler)
        self.workers.append(worker)
        logger.info(f"➕ Worker agregado: {worker_id} (Total: {len(self.workers)})")
    
    def remove_worker(self, worker_id: str) -> bool:
        """Remueve un worker del pool"""
        for i, worker in enumerate(self.workers):
            if worker.id == worker_id:
                self.workers.pop(i)
                logger.info(f"➖ Worker removido: {worker_id} (Total: {len(self.workers)})")
                return True
        return False
    
    def _select_worker_round_robin(self) -> Worker:
        """Selecciona worker usando round-robin"""
        if not self.workers:
            raise ValueError("No hay workers disponibles")
        
        worker = self.workers[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.workers)
        return worker
    
    def _select_worker_least_loaded(self) -> Worker:
        """Selecciona el worker con menos carga"""
        if not self.workers:
            raise ValueError("No hay workers disponibles")
        
        return min(self.workers, key=lambda w: w.current_load)
    
    def _select_worker_random(self) -> Worker:
        """Selecciona un worker aleatorio"""
        import random
        if not self.workers:
            raise ValueError("No hay workers disponibles")
        
        return random.choice(self.workers)
    
    def _select_worker(self) -> Worker:
        """Selecciona un worker según la estrategia"""
        if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            return self._select_worker_round_robin()
        elif self.strategy == LoadBalancingStrategy.LEAST_LOADED:
            return self._select_worker_least_loaded()
        elif self.strategy == LoadBalancingStrategy.RANDOM:
            return self._select_worker_random()
        else:
            return self._select_worker_round_robin()
    
    def process(self, task: Any) -> Any:
        """
        Procesa una tarea usando un worker del pool
        
        Args:
            task: Tarea a procesar
            
        Returns:
            Resultado del procesamiento
        """
        worker = self._select_worker()
        worker.current_load += 1
        
        start_time = time.time()
        
        try:
            logger.debug(f"⚙️  Worker {worker.id} procesando tarea (carga: {worker.current_load})")
            result = worker.handler(task)
            
            # Actualizar estadísticas
            processing_time = time.time() - start_time
            worker.total_processed += 1
            
            # Actualizar tiempo promedio
            if worker.avg_processing_time == 0:
                worker.avg_processing_time = processing_time
            else:
                worker.avg_processing_time = (
                    worker.avg_processing_time * 0.9 + processing_time * 0.1
                )
            
            logger.debug(f"✅ Worker {worker.id} completó tarea en {processing_time:.3f}s")
            return result
            
        except Exception as e:
            worker.total_errors += 1
            logger.error(f"❌ Worker {worker.id} error: {str(e)}")
            raise
        
        finally:
            worker.current_load -= 1
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas del balanceador"""
        if not self.workers:
            return {'workers': 0}
        
        total_processed = sum(w.total_processed for w in self.workers)
        total_errors = sum(w.total_errors for w in self.workers)
        avg_load = sum(w.current_load for w in self.workers) / len(self.workers)
        
        return {
            'workers': len(self.workers),
            'strategy': self.strategy.value,
            'total_processed': total_processed,
            'total_errors': total_errors,
            'error_rate': f"{(total_errors / total_processed * 100) if total_processed > 0 else 0:.2f}%",
            'avg_current_load': avg_load,
            'worker_stats': [
                {
                    'id': w.id,
                    'current_load': w.current_load,
                    'total_processed': w.total_processed,
                    'total_errors': w.total_errors,
                    'avg_processing_time': f"{w.avg_processing_time:.3f}s"
                }
                for w in self.workers
            ]
        }
    
    def print_stats(self):
        """Imprime estadísticas del balanceador"""
        stats = self.get_stats()
        
        print("\n" + "=" * 60)
        print("⚖️  ESTADÍSTICAS DEL BALANCEADOR")
        print("=" * 60)
        print(f"Workers activos: {stats['workers']}")
        print(f"Estrategia: {stats.get('strategy', 'N/A')}")
        print(f"Total procesado: {stats.get('total_processed', 0)}")
        print(f"Total errores: {stats.get('total_errors', 0)}")
        print(f"Tasa de error: {stats.get('error_rate', '0%')}")
        print(f"Carga promedio actual: {stats.get('avg_current_load', 0):.2f}")
        
        if 'worker_stats' in stats:
            print("\n📊 Workers:")
            for ws in stats['worker_stats']:
                print(f"  {ws['id']}:")
                print(f"    Carga actual: {ws['current_load']}")
                print(f"    Procesados: {ws['total_processed']}")
                print(f"    Errores: {ws['total_errors']}")
                print(f"    Tiempo prom: {ws['avg_processing_time']}")
        
        print("=" * 60 + "\n")

# Instancia global del balanceador
global_load_balancer = LoadBalancer()
