# src/app.py

import os
from flask import Flask

from src.modules import register_blueprints
from src.containers import AppContainer
from global_handler.middlewares.metrics_middleware import before_request_metrics, after_request_metrics
from global_handler.decorators.error_handler import register_error_handlers
from src.config import DEBUG, HOST, PORT


def create_app(container: AppContainer = None) -> Flask:
    # -------------------------
    # Path bootstrap
    # -------------------------
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )

    if project_root not in os.sys.path:
        os.sys.path.insert(0, project_root)

    app = Flask(__name__)

    # -------------------------
    # Dependency container
    # -------------------------
    app.container = container or AppContainer()

    # -------------------------
    # Register blueprints
    # -------------------------
    register_blueprints(app)

    # -------------------------
    # Middlewares
    # -------------------------
    app.before_request(before_request_metrics)
    app.after_request(after_request_metrics)

    # -------------------------
    # Error handlers
    # -------------------------
    register_error_handlers(app)

    return app


def run_server():
    app = create_app()
    app.run(
        debug=DEBUG,
        host=HOST,
        port=PORT
    )


if __name__ == "__main__":
    run_server()
