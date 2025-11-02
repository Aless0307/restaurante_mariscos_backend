"""
Sistema de caché simple en memoria para mejorar rendimiento
"""
from datetime import datetime, timedelta
from typing import Any, Optional
import json

class SimpleCache:
    """Caché simple en memoria con TTL (Time To Live)"""
    
    def __init__(self):
        self._cache = {}
        self._timestamps = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Obtener valor del caché si existe y no ha expirado"""
        if key in self._cache:
            timestamp = self._timestamps.get(key)
            if timestamp and datetime.now() < timestamp:
                return self._cache[key]
            else:
                # Cache expirado, eliminar
                self.delete(key)
        return None
    
    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        """
        Guardar valor en caché con TTL
        
        Args:
            key: Clave única para el valor
            value: Valor a almacenar
            ttl_seconds: Tiempo de vida en segundos (default: 5 minutos)
        """
        self._cache[key] = value
        self._timestamps[key] = datetime.now() + timedelta(seconds=ttl_seconds)
    
    def delete(self, key: str):
        """Eliminar una entrada del caché"""
        if key in self._cache:
            del self._cache[key]
        if key in self._timestamps:
            del self._timestamps[key]
    
    def clear(self):
        """Limpiar todo el caché"""
        self._cache.clear()
        self._timestamps.clear()
    
    def invalidate_pattern(self, pattern: str):
        """Invalidar todas las claves que contengan el patrón"""
        keys_to_delete = [key for key in self._cache.keys() if pattern in key]
        for key in keys_to_delete:
            self.delete(key)

# Instancia global del caché
cache = SimpleCache()
