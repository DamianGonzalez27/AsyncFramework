# -------------------------
# Copyright (c) 2026 Erick Damian Gonzalez Aranda
#
# Este software y su código fuente han sido desarrollados por Erick Damian Gonzalez Aranda, mediante 
# NeuronexoTec Organizacion de desarrollo de Software.
# Todos los derechos están reservados.
#
# Se permite el uso, copia y modificación del código únicamente para fines
# personales, educativos o internos, siempre que se conserve este aviso
# de copyright y no se redistribuya el software, total o parcialmente,
# sin autorización expresa del autor.
#
# Queda estrictamente prohibida la venta, sublicencia, redistribución,
# exposición como servicio (SaaS), o incorporación en productos comerciales
# sin consentimiento previo y por escrito del autor.
#
# Este software se proporciona "tal cual", sin garantía de ningún tipo,
# expresa o implícita, incluyendo pero no limitado a garantías de
# comercialización, idoneidad para un propósito particular o ausencia
# de defectos.
# 
# El autor no será responsable por ningún daño directo o indirecto
# derivado del uso de este software.
# -------------------------

"""
Puerto base para conexiones.

Define la interfaz común para todos los adaptadores de conexión.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class ConnectionStatus:
    """Estado de una conexión."""
    is_connected: bool = False
    last_connected: Optional[datetime] = None
    error_message: Optional[str] = None


class BasePort(ABC):
    """
    Clase base abstracta para todos los puertos de conexión.
    
    Define la interfaz común que todos los adaptadores deben implementar.
    """
    
    def __init__(self, port_type: str):
        """
        Inicializa el puerto.
        
        Args:
            port_type: Tipo de puerto (database, document, search, http, etc.)
        """
        self._port_type = port_type
        self._status = ConnectionStatus()
    
    @property
    def port_type(self) -> str:
        """Retorna el tipo de puerto."""
        return self._port_type
    
    @property
    def status(self) -> ConnectionStatus:
        """Retorna el estado de la conexión."""
        return self._status
    
    @abstractmethod
    def connect(self) -> Any:
        """
        Establece la conexión.
        
        Returns:
            El cliente de conexión
            
        Raises:
            ConnectionError: Si no se puede establecer la conexión
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Cierra la conexión."""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """
        Verifica si la conexión está activa.
        
        Returns:
            True si está conectado, False en caso contrario
        """
        pass