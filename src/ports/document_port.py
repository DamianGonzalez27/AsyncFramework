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
Puerto para bases de datos de documentos.

Define la interfaz para conectar con MongoDB, CouchDB, etc.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from src.ports.base_port import BasePort


@dataclass
class InsertResult:
    """Resultado de una operación de inserción."""
    inserted_id: str
    acknowledged: bool


@dataclass
class UpdateResult:
    """Resultado de una operación de actualización."""
    matched_count: int
    modified_count: int
    upserted_id: Optional[str] = None


@dataclass
class DeleteResult:
    """Resultado de una operación de eliminación."""
    deleted_count: int


class DocumentPort(BasePort):
    """
    Interfaz para bases de datos de documentos.
    
    Define las operaciones comunes para MongoDB, CouchDB, etc.
    """
    
    def __init__(self, port_type: str = "document"):
        super().__init__(port_type)
    
    # =========================================================================
    # Base de Datos
    # =========================================================================
    
    @abstractmethod
    def get_database(self, name: str) -> Any:
        """Obtiene una base de datos específica."""
        pass
    
    @abstractmethod
    def list_databases(self) -> List[str]:
        """Lista todas las bases de datos."""
        pass
    
    # =========================================================================
    # Colecciones
    # =========================================================================
    
    @abstractmethod
    def get_collection(self, collection: str) -> Any:
        """Obtiene una colección específica."""
        pass
    
    @abstractmethod
    def list_collections(self) -> List[str]:
        """Lista todas las colecciones."""
        pass
    
    @abstractmethod
    def create_collection(self, name: str) -> Any:
        """Crea una nueva colección."""
        pass
    
    @abstractmethod
    def drop_collection(self, name: str) -> bool:
        """Elimina una colección."""
        pass
    
    # =========================================================================
    # CRUD
    # =========================================================================
    
    @abstractmethod
    def find(
        self,
        collection: str,
        query: Dict[str, Any],
        projection: Optional[Dict[str, Any]] = None,
        limit: int = 0,
        skip: int = 0,
        sort: Optional[List[tuple]] = None
    ) -> List[Dict[str, Any]]:
        """Busca documentos en una colección."""
        pass
    
    @abstractmethod
    def find_one(
        self,
        collection: str,
        query: Dict[str, Any],
        projection: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Busca un solo documento."""
        pass
    
    @abstractmethod
    def insert_one(self, collection: str, document: Dict[str, Any]) -> InsertResult:
        """Inserta un documento."""
        pass
    
    @abstractmethod
    def insert_many(self, collection: str, documents: List[Dict[str, Any]]) -> List[InsertResult]:
        """Inserta múltiples documentos."""
        pass
    
    @abstractmethod
    def update_one(
        self,
        collection: str,
        query: Dict[str, Any],
        update: Dict[str, Any],
        upsert: bool = False
    ) -> UpdateResult:
        """Actualiza un documento."""
        pass
    
    @abstractmethod
    def update_many(
        self,
        collection: str,
        query: Dict[str, Any],
        update: Dict[str, Any],
        upsert: bool = False
    ) -> UpdateResult:
        """Actualiza múltiples documentos."""
        pass
    
    @abstractmethod
    def delete_one(self, collection: str, query: Dict[str, Any]) -> DeleteResult:
        """Elimina un documento."""
        pass
    
    @abstractmethod
    def delete_many(self, collection: str, query: Dict[str, Any]) -> DeleteResult:
        """Elimina múltiples documentos."""
        pass
    
    # =========================================================================
    # Agregaciones
    # =========================================================================
    
    @abstractmethod
    def aggregate(self, collection: str, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ejecuta un pipeline de agregación."""
        pass
    
    # =========================================================================
    # Índices
    # =========================================================================
    
    @abstractmethod
    def create_index(
        self,
        collection: str,
        keys: Dict[str, Any],
        unique: bool = False
    ) -> str:
        """Crea un índice en la colección."""
        pass
    
    @abstractmethod
    def list_indexes(self, collection: str) -> List[Dict[str, Any]]:
        """Lista los índices de una colección."""
        pass