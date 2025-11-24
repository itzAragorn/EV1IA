"""
IL3.4: Gestor de Caché
Sistema de caché para mejorar rendimiento y escalabilidad
"""

import time
import hashlib
from typing import Any, Optional, Dict
from dataclasses import dataclass
from ..observability.logger_config import get_logger
from ..observability.metrics_collector import global_metrics

logger = get_logger(__name__)

@dataclass
class CacheEntry:
    """Entrada de caché"""
    key: str
    value: Any
    timestamp: float
    ttl: float  # Time to live en segundos
    hits: int = 0
    
    @property
    def is_expired(self) -> bool:
        """Verifica si la entrada expiró"""
        return time.time() - self.timestamp > self.ttl
    
    @property
    def age(self) -> float:
        """Edad de la entrada en segundos"""
        return time.time() - self.timestamp

class CacheManager:
    """
    Gestor de caché para optimizar rendimiento
    Implementa IL3.4: Escalabilidad y Sostenibilidad
    """
    
    def __init__(self, default_ttl: float = 300.0, max_size: int = 1000):
        self.cache: Dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def _generate_key(self, key_data: str) -> str:
        """Genera una clave hash para el caché"""
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Obtiene un valor del caché
        
        Returns:
            Valor cacheado o None si no existe/expiró
        """
        cache_key = self._generate_key(key)
        
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            
            if entry.is_expired:
                # Entrada expirada, eliminar
                del self.cache[cache_key]
                self.misses += 1
                global_metrics.increment_counter('cache.miss', action='expired')
                logger.debug(f"🔴 Cache miss (expirado): {key[:50]}")
                return None
            
            # Cache hit
            entry.hits += 1
            self.hits += 1
            global_metrics.increment_counter('cache.hit')
            logger.debug(f"🟢 Cache hit: {key[:50]} (hits: {entry.hits})")
            return entry.value
        
        # Cache miss
        self.misses += 1
        global_metrics.increment_counter('cache.miss', action='not_found')
        logger.debug(f"🔴 Cache miss: {key[:50]}")
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None):
        """Almacena un valor en el caché"""
        cache_key = self._generate_key(key)
        
        # Verificar tamaño máximo
        if len(self.cache) >= self.max_size and cache_key not in self.cache:
            self._evict_lru()
        
        entry = CacheEntry(
            key=cache_key,
            value=value,
            timestamp=time.time(),
            ttl=ttl or self.default_ttl
        )
        
        self.cache[cache_key] = entry
        global_metrics.increment_counter('cache.set')
        logger.debug(f"💾 Cache set: {key[:50]} (TTL: {entry.ttl}s)")
    
    def _evict_lru(self):
        """Elimina la entrada menos usada recientemente (LRU)"""
        if not self.cache:
            return
        
        # Encontrar la entrada con menos hits y más antigua
        lru_key = min(
            self.cache.keys(),
            key=lambda k: (self.cache[k].hits, -self.cache[k].age)
        )
        
        del self.cache[lru_key]
        global_metrics.increment_counter('cache.eviction', strategy='lru')
        logger.debug(f"🗑️  Cache eviction (LRU): {lru_key}")
    
    def delete(self, key: str) -> bool:
        """Elimina una entrada del caché"""
        cache_key = self._generate_key(key)
        
        if cache_key in self.cache:
            del self.cache[cache_key]
            global_metrics.increment_counter('cache.delete')
            logger.debug(f"🗑️  Cache delete: {key[:50]}")
            return True
        
        return False
    
    def clear(self):
        """Limpia todo el caché"""
        count = len(self.cache)
        self.cache.clear()
        global_metrics.increment_counter('cache.clear')
        logger.info(f"🧹 Cache cleared: {count} entries removed")
    
    def clean_expired(self) -> int:
        """Limpia entradas expiradas"""
        expired_keys = [
            key for key, entry in self.cache.items()
            if entry.is_expired
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            global_metrics.increment_counter('cache.expired_cleaned', value=len(expired_keys))
            logger.info(f"🧹 Cleaned {len(expired_keys)} expired cache entries")
        
        return len(expired_keys)
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas del caché"""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f"{hit_rate:.2f}%",
            'total_requests': total_requests,
            'default_ttl': self.default_ttl
        }
    
    def print_stats(self):
        """Imprime estadísticas del caché"""
        stats = self.get_stats()
        
        print("\n" + "=" * 50)
        print("📊 ESTADÍSTICAS DE CACHÉ")
        print("=" * 50)
        print(f"Tamaño actual: {stats['size']}/{stats['max_size']}")
        print(f"Hits: {stats['hits']}")
        print(f"Misses: {stats['misses']}")
        print(f"Hit Rate: {stats['hit_rate']}")
        print(f"Total Requests: {stats['total_requests']}")
        print("=" * 50 + "\n")

# Instancia global del gestor de caché
global_cache_manager = CacheManager()
