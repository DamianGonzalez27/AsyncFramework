from flask import jsonify
from src.modules.payments.controllers import api_blueprint


@api_blueprint.route("/health", methods=["GET"])
def health_check():
    return jsonify({"module": "payments", "status": "healthy"}), 200
