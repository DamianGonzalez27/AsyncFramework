"""Servicio base del módulo de productos."""

from typing import Dict, Any, Optional


class ProductService:
    def __init__(self, repository: Optional[Any] = None):
        self.repository = repository

    def create_product(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        product = {
            "id": payload.get("id", "product-0001"),
            "name": payload.get("name", "default-product"),
            "price": payload.get("price", 0),
        }
        if self.repository is not None:
            self.repository.save(product)
        return product
