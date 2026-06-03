# Imagen base con Python
FROM python:3.13-slim

# Instala dependencias del sistema
# Instala dependencias del sistema
RUN apt-get update && apt-get install -y curl build-essential libmariadb-dev gcc && rm -rf /var/lib/apt/lists/*

# Crea directorio de trabajo
WORKDIR /app

# Copia archivos de Poetry y proyecto
COPY pyproject.toml poetry.lock* /app/

# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Exporta path de Poetry
ENV PATH="/root/.local/bin:$PATH"

# Instala dependencias
RUN poetry install --no-root --no-interaction --no-ansi

# Copia el resto del código
COPY . /app

#COPY ../.aws/ /.aws/

CMD ["poetry", "run", "worker"]
