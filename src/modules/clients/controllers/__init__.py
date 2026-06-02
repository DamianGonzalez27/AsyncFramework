from flask import Blueprint

# Crea un blueprint para el módulo de controladores
# El prefijo de URL opcional ayuda a organizar las rutas
api_blueprint = Blueprint('clients', __name__, url_prefix='/api/clients')

# Importa aquí tus controladores para que sean registrados en el blueprint
# Esto evita que tengas que importarlos manualmente en run_server.py
from src.modules.clients.controllers import clients_controller