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
Puerto para motores de búsqueda.

Define la interfaz para conectar con Elasticsearch, OpenSearch, Solr, etc.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from src.ports.base_port import BasePort


@dataclass
class SearchResult:
    """Resultado de una búsqueda."""
    hits: List[Dict[str, Any]]
    total: int
    took: int
    aggregations: Optional[Dict[str, Any]] = None


@dataclass
class IndexResult:
    """Resultado de una operación de indexación."""
    indexed: int
    errors: int
    failed_items: List[Any] = None


class SearchPort(BasePort):
    """
    Interfaz para motores de búsqueda.
    
    Define las operaciones comunes para Elasticsearch, OpenSearch, Solr, etc.
    """
    
    def __init__(self, port_type: str = "search"):
        super().__init__(port_type)
    
    # =========================================================================
    # Índices
    # =========================================================================
    
    @abstractmethod
    def create_index(
        self,
        index: str,
        settings: Optional[Dict[str, Any]] = None,
        mappings: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Crea un índice."""
        pass
    
    @abstractmethod
    def delete_index(self, index: str) -> bool:
        """Elimina un índice."""
        pass
    
    @abstractmethod
    def index_exists(self, index: str) -> bool:
        """Verifica si un índice existe."""
        pass
    
    @abstractmethod
    def list_indexes(self) -> List[str]:
        """Lista todos los índices."""
        pass
    
    @abstractmethod
    def get_index_mapping(self, index: str) -> Dict[str, Any]:
        """Obtiene el mapeo de un índice."""
        pass
    
    # =========================================================================
    # Indexación
    # =========================================================================
    
    @abstractmethod
    def index_document(
        self,
        index: str,
        document: Dict[str, Any],
        doc_id: Optional[str] = None
    ) -> str:
        """Indexa un documento."""
        pass
    
    @abstractmethod
    def index_documents(
        self,
        index: str,
        documents: List[Dict[str, Any]],
        doc_ids: Optional[List[str]] = None
    ) -> IndexResult:
        """Indexa múltiples documentos."""
        pass
    
    @abstractmethod
    def update_document(
        self,
        index: str,
        doc_id: str,
        document: Dict[str, Any]
    ) -> bool:
        """Actualiza un documento."""
        pass
    
    @abstractmethod
    def delete_document(self, index: str, doc_id: str) -> bool:
        """Elimina un documento."""
        pass
    
    # =========================================================================
    # Búsqueda
    # =========================================================================
    
    @abstractmethod
    def search(
        self,
        index: str,
        query: Dict[str, Any],
        from_: int = 0,
        size: int = 10,
        sort: Optional[List[Dict[str, Any]]] = None,
        highlight: Optional[Dict[str, Any]] = None,
        aggs: Optional[Dict[str, Any]] = None
    ) -> SearchResult:
        """Ejecuta una búsqueda."""
        pass
    
    @abstractmethod
    def search_by_id(self, index: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Busca un documento por su ID."""
        pass
    
    @abstractmethod
    def count(self, index: str, query: Optional[Dict[str, Any]] = None) -> int:
        """Cuenta documentos que coinciden con una consulta."""
        pass
    
    # =========================================================================
    # Agregaciones
    # =========================================================================
    
    @abstractmethod
    def aggregate(
        self,
        index: str,
        aggs: Dict[str, Any],
        query: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Ejecuta agregaciones."""
        pass
    
    # =========================================================================
    # Bulk
    # =========================================================================
    
    @abstractmethod
    def bulk(self, operations: List[Dict[str, Any]]) -> IndexResult:
        """Ejecuta operaciones en bulk."""
        pass
    
    # =========================================================================
    # Alias
    # =========================================================================
    
    @abstractmethod
    def create_alias(self, index: str, alias: str) -> bool:
        """Crea un alias para un índice."""
        pass
    
    @abstractmethod
    def delete_alias(self, index: str, alias: str) -> bool:
        """Elimina un alias."""
        pass
    
    @abstractmethod
    def list_aliases(self, index: Optional[str] = None) -> Dict[str, List[str]]:
        """Lista los alias disponibles."""
        pass