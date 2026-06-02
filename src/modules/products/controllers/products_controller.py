from flask import jsonify
from src.modules.products.controllers import api_blueprint


@api_blueprint.route("/health", methods=["GET"])
def health_check():
    return jsonify({"module": "products", "status": "healthy"}), 200
