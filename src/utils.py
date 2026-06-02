from src.config import (
    DATABASE_URL,
    DB_DRIVER,
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
)


# -------------------------
# Construcción de la URL de conexión a la base de datos
#
# Utiliza las variables de configuración del proyecto.
# Falla explícitamente si falta algún valor requerido.
# -------------------------

def get_database_url():
    if DATABASE_URL:
        return DATABASE_URL

    driver = DB_DRIVER
    user = DB_USER
    password = DB_PASSWORD
    host = DB_HOST
    port = DB_PORT
    database = DB_NAME

    if not all([driver, user, password, host, port, database]):
        raise RuntimeError(
            "Faltan valores en la configuración de 'database' para Alembic"
        )

    return f"{driver}://{user}:{password}@{host}:{port}/{database}"