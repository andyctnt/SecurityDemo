# Dockerfile
FROM alpine:latest

# Actualiza el repositorio de paquetes e instala Nmap y Python
RUN apk update && apk add nmap python3 py3-pip

# Instala la librería de InfluxDB para Python
RUN pip3 install influxdb

# Copia el script al contenedor
COPY nmap_to_influx.py /nmap_to_influx.py

# Define el punto de entrada
ENTRYPOINT ["python3", "/nmap_to_influx.py"]

