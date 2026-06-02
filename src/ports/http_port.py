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
Puerto para APIs HTTP/REST.

Define la interfaz para realizar solicitudes HTTP.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Optional

from src.ports.base_port import BasePort


class HTTPMethod(Enum):
    """Métodos HTTP soportados."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


@dataclass
class HTTPResponse:
    """Respuesta de una solicitud HTTP."""
    status_code: int
    headers: Dict[str, str]
    body: str
    elapsed_time: float  # en milisegundos


@dataclass
class HTTPCredentials:
    """Credenciales para autenticación HTTP."""
    auth_type: str  # basic, bearer, api_key
    credentials: Optional[Dict[str, str]] = None


class HTTPPort(BasePort):
    """
    Interfaz para APIs HTTP/REST.
    
    Define las operaciones comunes para realizar solicitudes HTTP.
    """
    
    def __init__(self, port_type: str = "http"):
        super().__init__(port_type)
        self._base_url: Optional[str] = None
        self._default_headers: Dict[str, str] = {}
        self._credentials: Optional[HTTPCredentials] = None
    
    # =========================================================================
    # Configuración
    # =========================================================================
    
    @abstractmethod
    def set_base_url(self, base_url: str) -> None:
        """Establece la URL base."""
        pass
    
    @abstractmethod
    def set_headers(self, headers: Dict[str, str]) -> None:
        """Establece headers por defecto."""
        pass
    
    @abstractmethod
    def set_credentials(self, credentials: HTTPCredentials) -> None:
        """Establece credenciales de autenticación."""
        pass
    
    @abstractmethod
    def set_timeout(self, timeout: float) -> None:
        """Establece el timeout."""
        pass
    
    # =========================================================================
    # Métodos HTTP
    # =========================================================================
    
    @abstractmethod
    def request(
        self,
        method: HTTPMethod,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> HTTPResponse:
        """Realiza una solicitud HTTP genérica."""
        pass
    
    @abstractmethod
    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> HTTPResponse:
        """Realiza una solicitud GET."""
        pass
    
    @abstractmethod
    def post(
        self,
        path: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> HTTPResponse:
        """Realiza una solicitud POST."""
        pass
    
    @abstractmethod
    def put(
        self,
        path: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> HTTPResponse:
        """Realiza una solicitud PUT."""
        pass
    
    @abstractmethod
    def patch(
        self,
        path: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> HTTPResponse:
        """Realiza una solicitud PATCH."""
        pass
    
    @abstractmethod
    def delete(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> HTTPResponse:
        """Realiza una solicitud DELETE."""
        pass
    
    # =========================================================================
    # Utility
    # =========================================================================
    
    @abstractmethod
    def head(self, path: str) -> HTTPResponse:
        """Realiza una solicitud HEAD."""
        pass
    
    @abstractmethod
    def options(self, path: str) -> HTTPResponse:
        """Realiza una solicitud OPTIONS."""
        pass
    
    @abstractmethod
    def download(self, path: str, destination: str, params: Optional[Dict[str, Any]] = None) -> bool:
        """Descarga un archivo."""
        pass
    
    @abstractmethod
    def upload(
        self,
        path: str,
        file_path: str,
        field_name: str = "file",
        data: Optional[Dict[str, Any]] = None
    ) -> HTTPResponse:
        """Sube un archivo."""
        pass