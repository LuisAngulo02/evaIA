"""
Gestor Inteligente de API Keys de Groq
======================================
Sistema de rotación automática de múltiples API keys.
Si una key se queda sin tokens o falla, cambia automáticamente a la siguiente.

Características:
- Rotación automática ante rate limits
- Cache de keys fallidas (evita reintentos innecesarios)
- Reset automático de keys después de 60 segundos
- Logging detallado de cambios de key
"""

import os
import time
from typing import Optional, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class GroqKeyManager:
    """
    Gestor de rotación automática de API keys de Groq.
    
    Funcionalidades:
    1. Carga múltiples keys desde variables de entorno
    2. Rotación automática cuando una key falla
    3. Cache temporal de keys fallidas (60s)
    4. Estadísticas de uso por key
    """
    
    def __init__(self):
        """Inicializa el gestor cargando todas las keys disponibles."""
        self.keys = self._load_keys()
        self.current_key_index = 0
        self.failed_keys = {}  # {key: timestamp_when_failed}
        self.key_stats = {key: {'requests': 0, 'failures': 0} for key in self.keys}
        self.reset_timeout = 60  # Segundos antes de reintentar una key fallida
        
        if self.keys:
            logger.info(f"🔑 Gestor de Groq iniciado con {len(self.keys)} API keys disponibles")
        else:
            logger.warning("⚠️ No se encontraron API keys de Groq configuradas")
    
    def _load_keys(self) -> List[str]:
        """
        Carga todas las API keys desde variables de entorno.
        
        Busca:
        - GROQ_API_KEY_1, GROQ_API_KEY_2, ..., GROQ_API_KEY_N
        - GROQ_API_KEY (fallback)
        
        Returns:
            Lista de API keys válidas (no vacías)
        """
        keys = []
        
        # Intentar cargar keys numeradas (1-10)
        for i in range(1, 11):
            key = os.getenv(f'GROQ_API_KEY_{i}', '').strip()
            if key and key not in keys:
                keys.append(key)
        
        # Si no hay keys numeradas, intentar key única
        if not keys:
            key = os.getenv('GROQ_API_KEY', '').strip()
            if key:
                keys.append(key)
        
        return keys
    
    def get_current_key(self) -> Optional[str]:
        """
        Obtiene la API key actual válida.
        
        Salta automáticamente las keys que han fallado recientemente.
        
        Returns:
            API key válida o None si no hay keys disponibles
        """
        if not self.keys:
            return None
        
        # Limpiar keys fallidas antiguas (> reset_timeout segundos)
        self._cleanup_failed_keys()
        
        # Buscar una key válida (no fallida)
        attempts = 0
        max_attempts = len(self.keys)
        
        while attempts < max_attempts:
            current_key = self.keys[self.current_key_index]
            
            # Verificar si la key está disponible
            if current_key not in self.failed_keys:
                # Incrementar contador de uso
                self.key_stats[current_key]['requests'] += 1
                return current_key
            
            # Key fallida, probar la siguiente
            self.current_key_index = (self.current_key_index + 1) % len(self.keys)
            attempts += 1
        
        # Todas las keys han fallado recientemente
        logger.warning("⚠️ Todas las API keys de Groq están temporalmente bloqueadas")
        logger.info(f"⏱️ Las keys se resetearán en {self.reset_timeout}s")
        return None
    
    def mark_key_as_failed(self, key: str, error_message: str = ""):
        """
        Marca una key como fallida temporalmente.
        
        La key será evitada durante reset_timeout segundos.
        
        Args:
            key: API key que falló
            error_message: Mensaje de error (opcional)
        """
        if key in self.keys:
            self.failed_keys[key] = time.time()
            self.key_stats[key]['failures'] += 1
            
            key_index = self.keys.index(key) + 1
            logger.warning(f"❌ API Key #{key_index} falló: {error_message}")
            logger.info(f"🔄 Rotando a siguiente key...")
            
            # Rotar a la siguiente key
            self._rotate_to_next_key()
    
    def _rotate_to_next_key(self):
        """Rota al siguiente índice de key disponible."""
        self.current_key_index = (self.current_key_index + 1) % len(self.keys)
        
        new_key = self.keys[self.current_key_index]
        if new_key not in self.failed_keys:
            key_index = self.current_key_index + 1
            logger.info(f"✅ Cambiado a API Key #{key_index}")
    
    def _cleanup_failed_keys(self):
        """
        Limpia keys fallidas que han superado el timeout de reset.
        
        Permite reintentar keys después de reset_timeout segundos.
        """
        current_time = time.time()
        keys_to_remove = []
        
        for key, failed_time in self.failed_keys.items():
            if current_time - failed_time > self.reset_timeout:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.failed_keys[key]
            key_index = self.keys.index(key) + 1
            logger.info(f"🔓 API Key #{key_index} desbloqueada y lista para usar")
    
    def get_stats(self) -> dict:
        """
        Obtiene estadísticas de uso de las keys.
        
        Returns:
            Dict con estadísticas por key:
            {
                'total_keys': int,
                'active_keys': int,
                'failed_keys': int,
                'key_details': [...]
            }
        """
        stats = {
            'total_keys': len(self.keys),
            'active_keys': len(self.keys) - len(self.failed_keys),
            'failed_keys': len(self.failed_keys),
            'key_details': []
        }
        
        for i, key in enumerate(self.keys):
            key_masked = f"{key[:8]}...{key[-8:]}"
            is_current = (i == self.current_key_index)
            is_failed = key in self.failed_keys
            
            stats['key_details'].append({
                'index': i + 1,
                'key_preview': key_masked,
                'is_current': is_current,
                'is_failed': is_failed,
                'requests': self.key_stats[key]['requests'],
                'failures': self.key_stats[key]['failures']
            })
        
        return stats
    
    def print_stats(self):
        """Imprime estadísticas de uso en consola."""
        stats = self.get_stats()
        
        print("\n" + "="*60)
        print("📊 ESTADÍSTICAS DE API KEYS DE GROQ")
        print("="*60)
        print(f"Total de keys: {stats['total_keys']}")
        print(f"Keys activas: {stats['active_keys']}")
        print(f"Keys bloqueadas: {stats['failed_keys']}")
        print("\nDetalle por key:")
        print("-"*60)
        
        for detail in stats['key_details']:
            status = "🟢 ACTIVA" if not detail['is_failed'] else "🔴 BLOQUEADA"
            current_marker = " ← ACTUAL" if detail['is_current'] else ""
            
            print(f"Key #{detail['index']}: {detail['key_preview']}")
            print(f"  Estado: {status}{current_marker}")
            print(f"  Requests: {detail['requests']} | Fallos: {detail['failures']}")
            print()
        
        print("="*60 + "\n")


# Instancia global del gestor
_groq_key_manager = None


def get_groq_key_manager() -> GroqKeyManager:
    """
    Obtiene la instancia global del gestor de keys (singleton).
    
    Returns:
        Instancia de GroqKeyManager
    """
    global _groq_key_manager
    
    if _groq_key_manager is None:
        _groq_key_manager = GroqKeyManager()
    
    return _groq_key_manager


def get_groq_api_key() -> Optional[str]:
    """
    Función de conveniencia para obtener la API key actual.
    
    Returns:
        API key válida o None
    """
    manager = get_groq_key_manager()
    return manager.get_current_key()
