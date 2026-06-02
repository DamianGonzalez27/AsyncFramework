# -------------------------
# Copyright (c) 2026 Erick Damian Gonzalez Aranda
# -------------------------

"""Adaptador para Elasticsearch.

Implementa la conexión y operaciones con Elasticsearch mediante elasticsearch-py.
"""

from typing import Dict, Any, List, Optional
from logger_tracker import logg_info, logg_error, logg_debug


class ElasticsearchAdapter:
    """Adaptador concreto para conexiones a Elasticsearch."""

    def __init__(
        self,
        hosts: List[str] = None,
        scheme: str = "http",
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: int = 30,
    ):
        self.hosts = hosts or ["localhost:9200"]
        self.scheme = scheme
        self.username = username
        self.password = password
        self.timeout = timeout
        self.client = None

    def connect(self) -> None:
        """Establece conexión con Elasticsearch."""
        try:
            from elasticsearch import Elasticsearch

            es_config = {
                "hosts": self.hosts,
                "scheme": self.scheme,
                "timeout": self.timeout,
            }

            if self.username and self.password:
                es_config["basic_auth"] = (self.username, self.password)

            self.client = Elasticsearch(**es_config)
            self.client.info()
            logg_info(f"✓ Elasticsearch connected: {self.hosts}")
        except Exception as e:
            logg_error(f"✗ Failed to connect to Elasticsearch: {e}")
            raise

    def create_index(
        self,
        index_name: str,
        mappings: Optional[Dict[str, Any]] = None,
        settings: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Crea un índice en Elasticsearch."""
        try:
            if not self.client:
                raise RuntimeError("Not connected to Elasticsearch")

            body = {}
            if settings:
                body["settings"] = settings
            if mappings:
                body["mappings"] = mappings

            self.client.indices.create(index=index_name, body=body if body else None)
            logg_info(f"Index created: {index_name}")
        except Exception as e:
            logg_error(f"Failed to create index {index_name}: {e}")
            raise

    def delete_index(self, index_name: str) -> None:
        """Elimina un índice de Elasticsearch."""
        try:
            if not self.client:
                raise RuntimeError("Not connected to Elasticsearch")
            self.client.indices.delete(index=index_name)
            logg_info(f"Index deleted: {index_name}")
        except Exception as e:
            logg_error(f"Failed to delete index {index_name}: {e}")
            raise

    def index_document(
        self,
        index_name: str,
        doc_id: Optional[str] = None,
        body: Dict[str, Any] = None,
    ) -> str:
        """Indexa un documento en Elasticsearch."""
        try:
            if not self.client:
                raise RuntimeError("Not connected to Elasticsearch")
            result = self.client.index(index=index_name, id=doc_id, body=body)
            logg_debug(f"Document indexed in {index_name}")
            return result["_id"]
        except Exception as e:
            logg_error(f"Failed to index document in {index_name}: {e}")
            raise

    def search(
        self, index_name: str, query: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Busca documentos en Elasticsearch."""
        try:
            if not self.client:
                raise RuntimeError("Not connected to Elasticsearch")
            result = self.client.search(index=index_name, query=query)
            logg_debug(f"Search performed on {index_name}")
            return result
        except Exception as e:
            logg_error(f"Failed to search in {index_name}: {e}")
            raise

    def get_document(self, index_name: str, doc_id: str) -> Dict[str, Any]:
        """Obtiene un documento por ID."""
        try:
            if not self.client:
                raise RuntimeError("Not connected to Elasticsearch")
            result = self.client.get(index=index_name, id=doc_id)
            logg_debug(f"Document retrieved from {index_name}")
            return result
        except Exception as e:
            logg_error(f"Failed to get document {doc_id} from {index_name}: {e}")
            raise

    def delete_document(self, index_name: str, doc_id: str) -> None:
        """Elimina un documento de Elasticsearch."""
        try:
            if not self.client:
                raise RuntimeError("Not connected to Elasticsearch")
            self.client.delete(index=index_name, id=doc_id)
            logg_info(f"Document deleted from {index_name}")
        except Exception as e:
            logg_error(f"Failed to delete document {doc_id}: {e}")
            raise

    def close(self) -> None:
        """Cierra la conexión con Elasticsearch."""
        try:
            if self.client:
                self.client.close()
                logg_info("✓ Elasticsearch connection closed")
        except Exception as e:
            logg_error(f"Error closing Elasticsearch connection: {e}")
