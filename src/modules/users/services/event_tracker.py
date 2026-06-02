#
# Event Tracker Service
#
from logger_tracker import logg_info
#
# Create event function
# Esta funcion tiene el objetivo de generar un registro en la base de datos
# Recibe los datos de un evento en formato de modelo 
# Retorna el ID del evento creado
#
def create_event(event_data):
    logg_info("Creating event...")
    # Lógica para crear un evento
    pass

def get_event(event_id):
    logg_info(f"Getting event with ID: {event_id}")
    # Lógica para obtener un evento por ID
    pass

def update_event(event_id, event_data):
    logg_info(f"Updating event with ID: {event_id}")
    # Lógica para actualizar un evento por ID
    pass