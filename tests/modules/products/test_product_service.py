from src.modules.products.services.product_service import ProductService


def test_create_product_returns_default_values():
    service = ProductService()
    result = service.create_product({"name": "Example"})

    assert result["id"].startswith("product-")
    assert result["name"] == "Example"
    assert result["price"] == 0
