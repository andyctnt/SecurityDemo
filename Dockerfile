# Dockerfile
FROM ubuntu:latest

# Actualiza el repositorio de paquetes e instala dependencias necesarias
RUN apt-get update && apt-get install -y \
    nmap \
    python3 \
    python3-pip \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    mysql-client \
    bash \
    && apt-get clean

# Crear un entorno virtual y activarlo
RUN python3 -m venv /venv

# Activar el entorno virtual e instalar la librería de MySQL para Python
RUN /venv/bin/pip install --no-cache-dir mysql-connector-python

# Copiar el script al contenedor
COPY nmap_to_mysql.py /nmap_to_mysql.py
COPY wait-for-it.sh /wait-for-it.sh

# Hacer que el script wait-for-it.sh sea ejecutable
RUN chmod +x /wait-for-it.sh

# Definir el entorno virtual en el PATH
ENV PATH="/venv/bin:$PATH"

# Define el punto de entrada
ENTRYPOINT ["/wait-for-it.sh", "mysql:3306", "--", "python3", "/nmap_to_mysql.py"]
