"""Handlers para eventos del dominio de productos."""

from typing import Any, Dict

from logger_tracker import logg_info, logg_error

from src.modules.products.services.product_service import ProductService


class ProductHandler:
    """Procesa eventos relacionados con productos."""

    @staticmethod
    async def handle_created(payload: Dict[str, Any], **kwargs) -> None:
        logg_info(f"ProductHandler: processing product.created - {payload.get('name', 'unknown')}")
        service = ProductService()
        try:
            result = service.create_product(payload)
            logg_info(f"ProductHandler: product created - id={result.get('id')}")
        except Exception as e:
            logg_error(f"ProductHandler: error creating product - {e}")
            raise

    @staticmethod
    async def handle_updated(payload: Dict[str, Any], **kwargs) -> None:
        logg_info(f"ProductHandler: processing product.updated - {payload.get('id', 'unknown')}")
