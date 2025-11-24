"""
IL3.3: Limitador de Tasa
Sistema para prevenir abuso mediante rate limiting
"""

import time
from typing import Dict, Optional
from dataclasses import dataclass
from ..observability.logger_config import get_logger

logger = get_logger(__name__)

@dataclass
class RateLimit:
    """Configuración de límite de tasa"""
    max_requests: int
    time_window: float  # en segundos
    
class RateLimiter:
    """
    Limitador de tasa para prevenir abuso del sistema
    Implementa IL3.3: Seguridad
    """
    
    def __init__(self):
        self.user_requests: Dict[str, list] = {}
        self.limits: Dict[str, RateLimit] = {
            'default': RateLimit(max_requests=60, time_window=60.0),  # 60 req/min
            'query': RateLimit(max_requests=30, time_window=60.0),    # 30 queries/min
            'generation': RateLimit(max_requests=10, time_window=60.0)  # 10 gen/min
        }
    
    def check_rate_limit(self, user_id: str, action: str = 'default') -> tuple[bool, Optional[str]]:
        """
        Verifica si un usuario excedió el límite de tasa
        
        Args:
            user_id: Identificador del usuario
            action: Tipo de acción (default, query, generation)
            
        Returns:
            (allowed, message): Tupla indicando si se permite y mensaje
        """
        current_time = time.time()
        limit = self.limits.get(action, self.limits['default'])
        
        # Obtener o crear registro del usuario
        key = f"{user_id}:{action}"
        if key not in self.user_requests:
            self.user_requests[key] = []
        
        # Limpiar requests antiguos
        self.user_requests[key] = [
            req_time for req_time in self.user_requests[key]
            if current_time - req_time < limit.time_window
        ]
        
        # Verificar límite
        if len(self.user_requests[key]) >= limit.max_requests:
            remaining_time = limit.time_window - (current_time - self.user_requests[key][0])
            logger.warning(
                f"🚫 Rate limit excedido para usuario {user_id} en acción '{action}'",
                extra={'user_id': user_id, 'action': action}
            )
            return False, f"Límite de tasa excedido. Intente nuevamente en {remaining_time:.0f} segundos."
        
        # Registrar nueva solicitud
        self.user_requests[key].append(current_time)
        return True, None
    
    def record_request(self, user_id: str, action: str = 'default'):
        """Registra una solicitud de usuario"""
        key = f"{user_id}:{action}"
        if key not in self.user_requests:
            self.user_requests[key] = []
        self.user_requests[key].append(time.time())
    
    def get_user_stats(self, user_id: str) -> Dict:
        """Obtiene estadísticas de uso de un usuario"""
        current_time = time.time()
        stats = {}
        
        for action, limit in self.limits.items():
            key = f"{user_id}:{action}"
            if key in self.user_requests:
                recent_requests = [
                    req_time for req_time in self.user_requests[key]
                    if current_time - req_time < limit.time_window
                ]
                stats[action] = {
                    'requests_in_window': len(recent_requests),
                    'max_requests': limit.max_requests,
                    'time_window': limit.time_window,
                    'remaining': max(0, limit.max_requests - len(recent_requests))
                }
            else:
                stats[action] = {
                    'requests_in_window': 0,
                    'max_requests': limit.max_requests,
                    'time_window': limit.time_window,
                    'remaining': limit.max_requests
                }
        
        return stats
    
    def set_custom_limit(self, action: str, max_requests: int, time_window: float):
        """Establece un límite personalizado para una acción"""
        self.limits[action] = RateLimit(max_requests=max_requests, time_window=time_window)
        logger.info(f"⚙️  Límite personalizado establecido: {action} = {max_requests} req/{time_window}s")
    
    def reset_user_limits(self, user_id: str):
        """Resetea los límites de un usuario"""
        keys_to_remove = [key for key in self.user_requests.keys() if key.startswith(f"{user_id}:")]
        for key in keys_to_remove:
            del self.user_requests[key]
        logger.info(f"🔄 Límites reseteados para usuario: {user_id}")
    
    def get_global_stats(self) -> Dict:
        """Obtiene estadísticas globales del sistema"""
        total_users = len(set(key.split(':')[0] for key in self.user_requests.keys()))
        total_requests = sum(len(requests) for requests in self.user_requests.values())
        
        return {
            'total_users': total_users,
            'total_requests_tracked': total_requests,
            'active_limits': len(self.limits)
        }

# Instancia global del limitador
global_rate_limiter = RateLimiter()
