from flask import Blueprint

api_blueprint = Blueprint(
    "products",
    __name__,
    url_prefix="/api/products",
)

from src.modules.products.controllers import products_controller
