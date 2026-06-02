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
Puerto para bases de datos relacionales.

Define la interfaz para conectar con PostgreSQL, MySQL, SQLite, etc.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from src.ports.base_port import BasePort


class DatabasePort(BasePort):
    """
    Interfaz para bases de datos relacionales.
    
    Define las operaciones comunes para PostgreSQL, MySQL, SQLite, etc.
    """
    
    def __init__(self, port_type: str = "database"):
        super().__init__(port_type)
    
    # =========================================================================
    # Transacciones
    # =========================================================================
    
    @abstractmethod
    def begin(self) -> Session:
        """Inicia una nueva transacción."""
        pass
    
    @abstractmethod
    def commit(self, session: Session) -> None:
        """Confirma una transacción."""
        pass
    
    @abstractmethod
    def rollback(self, session: Session) -> None:
        """Revierte una transacción."""
        pass
    
    # =========================================================================
    # Metadata
    # =========================================================================
    
    @abstractmethod
    def get_tables(self) -> List[str]:
        """Obtiene la lista de tablas."""
        pass
    
    @abstractmethod
    def get_columns(self, table: str) -> List[Dict[str, Any]]:
        """Obtiene las columnas de una tabla."""
        pass
    
    @abstractmethod
    def get_primary_keys(self, table: str) -> List[str]:
        """Obtiene las claves primarias de una tabla."""
        pass
    
    @abstractmethod
    def get_foreign_keys(self, table: str) -> List[Dict[str, Any]]:
        """Obtiene las claves foráneas de una tabla."""
        pass
    
    # =========================================================================
    # CRUD
    # =========================================================================
    
    @abstractmethod
    def execute(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        session: Optional[Session] = None
    ) -> List[Dict[str, Any]]:
        """Ejecuta una consulta SQL."""
        pass
    
    @abstractmethod
    def execute_raw(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Ejecuta una consulta raw sin resultados."""
        pass
    
    # =========================================================================
    # Utilidades
    # =========================================================================
    
    @abstractmethod
    def table_exists(self, table: str) -> bool:
        """Verifica si una tabla existe."""
        pass
    
    @abstractmethod
    def database_exists(self, database: str) -> bool:
        """Verifica si una base de datos existe."""
        pass