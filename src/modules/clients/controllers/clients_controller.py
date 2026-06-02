from flask import jsonify
from src.modules.clients.controllers import api_blueprint


@api_blueprint.route("/health", methods=["GET"])
def health_check():
    return jsonify({"module": "clients", "status": "healthy"}), 200
        