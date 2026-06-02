"""Módulo de clientes.

Este paquete agrupa los componentes del dominio de clientes:
controladores, repositorios, modelos y servicios.
"""

from src.modules.clients.controllers import api_blueprint

__all__ = ["api_blueprint"]
