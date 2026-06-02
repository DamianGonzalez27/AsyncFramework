from global_handler.controllers.base_controller import BaseController

from src.modules.products.controllers import api_blueprint

base_controller = BaseController()


@api_blueprint.route("/health", methods=["GET"])
def health_check():
    return base_controller.success(
        message="Products module healthy",
        data={"module": "products", "status": "healthy"},
    )
