from flask import Blueprint

api_blueprint = Blueprint(
    "payments",
    __name__,
    url_prefix="/api/payments",
)

from src.modules.payments.controllers import payments_controller
