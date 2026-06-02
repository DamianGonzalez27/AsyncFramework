from flask import jsonify
from src.modules.users.controllers import api_blueprint


@api_blueprint.route("/health", methods=["GET"])
def health_check():
    return jsonify({"module": "users", "status": "healthy"}), 200
