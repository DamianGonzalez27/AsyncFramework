from flask import Flask

from src.modules.clients.controllers import api_blueprint as clients_blueprint
from src.modules.payments.controllers import api_blueprint as payments_blueprint
from src.modules.products.controllers import api_blueprint as products_blueprint
from src.modules.users.controllers import api_blueprint as users_blueprint

MODULE_BLUEPRINTS = [
    clients_blueprint,
    payments_blueprint,
    products_blueprint,
    users_blueprint,
]


def register_blueprints(app: Flask) -> None:
    """Registra los blueprints de cada módulo en la aplicación."""
    for blueprint in MODULE_BLUEPRINTS:
        app.register_blueprint(blueprint)
