# Dockerfile
FROM alpine:latest

# Actualiza el repositorio de paquetes e instala dependencias necesarias
RUN apk update && apk add --no-cache \
    nmap \
    python3 \
    py3-pip \
    build-base \
    libffi-dev \
    openssl-dev \
    python3-dev \
    mysql-client \
    mariadb-connector-c-dev \
    py3-virtualenv

# Crear un entorno virtual y activarlo
RUN python3 -m venv /venv

# Activar el entorno virtual e instalar la librería de MySQL para Python
RUN /venv/bin/pip install --no-cache-dir mysql-connector-python

# Copiar el script al contenedor
COPY nmap_to_mysql.py /nmap_to_mysql.py

# Definir el entorno virtual en el PATH
ENV PATH="/venv/bin:$PATH"

# Define el punto de entrada
ENTRYPOINT ["python3", "/nmap_to_mysql.py"]
