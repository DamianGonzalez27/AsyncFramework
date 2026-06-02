from flask import Blueprint

api_blueprint = Blueprint(
    "users",
    __name__,
    url_prefix="/api/users",
)

from src.modules.users.controllers import users_controller
