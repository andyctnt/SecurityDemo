import subprocess
from influxdb import InfluxDBClient
import xml.etree.ElementTree as ET
import os
import time

# Configuración de InfluxDB
influxdb_host = os.getenv('INFLUXDB_HOST', 'localhost')
influxdb_port = int(os.getenv('INFLUXDB_PORT', '8086'))
influxdb_user = os.getenv('INFLUXDB_USER', 'nmap_user')
influxdb_password = os.getenv('INFLUXDB_PASSWORD', 'beonitdemo')
influxdb_db = os.getenv('INFLUXDB_DB', 'nmap')

client = InfluxDBClient(host=influxdb_host, port=influxdb_port, username=influxdb_user, password=influxdb_password, database=influxdb_db)

# Función para ejecutar Nmap y procesar los resultados
def run_nmap():
    result = subprocess.run(['nmap', '-oX', '-', '192.168.1.0/24'], stdout=subprocess.PIPE)
    xml_output = result.stdout.decode()
    root = ET.fromstring(xml_output)
    json_body = []

    for host in root.findall('host'):
        address = host.find('address').get('addr')
        status = host.find('status').get('state')
        json_body.append({
            "measurement": "nmap_scan",
            "tags": {
                "host": address
            },
            "fields": {
                "status": status
            }
        })

    if json_body:
        client.write_points(json_body)

# Ejecutar Nmap periódicamente
while True:
    run_nmap()
    time.sleep(3600)  # Ejecuta cada hora
