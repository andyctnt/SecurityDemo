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

# Función para leer las IPs del archivo listado.list
def read_target_ips(file_path='/listado.list'):
    with open(file_path, 'r') as file:
        ips = [line.strip() for line in file.readlines() if line.strip()]
    return ips

# Función para ejecutar Nmap y procesar los resultados
def run_nmap(target_ips):
    ip_range = ' '.join(target_ips)
    nmap_command = ['nmap', '-sV', '-F', '--script=http-title,ssl-cert', '-oX', 'myoutput.xml', ip_range]
    result = subprocess.run(nmap_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Leer el archivo myoutput.xml
    with open('myoutput.xml', 'r') as xml_file:
        xml_output = xml_file.read()
    
    root = ET.fromstring(xml_output)
    json_body = []

    for host in root.findall('host'):
        address = host.find('address').get('addr')
        status = host.find('status').get('state')
        for port in host.findall('ports/port'):
            port_id = port.get('portid')
            protocol = port.get('protocol')
            service = port.find('service')
            service_name = service.get('name') if service is not None else 'unknown'
            service_version = service.get('version') if service is not None else 'unknown'
            http_title = ''
            ssl_cert = ''

            # Extraer información del script de Nmap
            for script in port.findall('script'):
                if script.get('id') == 'http-title':
                    http_title = script.get('output')
                elif script.get('id') == 'ssl-cert':
                    ssl_cert = script.get('output')
            
            json_body.append({
                "measurement": "nmap_scan",
                "tags": {
                    "host": address,
                    "port": port_id,
                    "protocol": protocol,
                    "service": service_name
                },
                "fields": {
                    "status": status,
                    "service_version": service_version,
                    "http_title": http_title,
                    "ssl_cert": ssl_cert
                }
            })

    if json_body:
        client.write_points(json_body)

# Ejecutar Nmap periódicamente
def main():
    while True:
        target_ips = read_target_ips()
        run_nmap(target_ips)
        time.sleep(3600)  # Ejecuta cada hora

if __name__ == "__main__":
    main()
