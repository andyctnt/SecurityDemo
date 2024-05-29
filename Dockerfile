FROM alpine:latest

# Actualiza el repositorio de paquetes e instala Nmap
RUN apk update && apk add nmap

# Define el punto de entrada
ENTRYPOINT ["nmap"]
