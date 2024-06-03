import subprocess
import mysql.connector
import xml.etree.ElementTree as ET
import os
import time

# Configuración de MySQL
mysql_host = os.getenv('MYSQL_HOST', 'localhost')
mysql_port = int(os.getenv('MYSQL_PORT', '3306'))
mysql_user = os.getenv('MYSQL_USER', 'nmap_user')
mysql_password = os.getenv('MYSQL_PASSWORD', 'yourpassword')
mysql_db = os.getenv('MYSQL_DB', 'nmap')

# Conectar a la base de datos MySQL
conn = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_db
)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS nmap_scan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    host VARCHAR(255),
    port INT,
    protocol VARCHAR(10),
    service VARCHAR(255),
    service_version VARCHAR(255),
    http_title TEXT,
    ssl_cert TEXT,
    scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

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
            
            # Insertar datos en la base de datos
            cursor.execute("""
            INSERT INTO nmap_scan (host, port, protocol, service, service_version, http_title, ssl_cert)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (address, port_id, protocol, service_name, service_version, http_title, ssl_cert))
    
    conn.commit()

# Ejecutar Nmap periódicamente
def main():
    while True:
        target_ips = read_target_ips()
        run_nmap(target_ips)
        time.sleep(3600)  # Ejecuta cada hora

if __name__ == "__main__":
    main()
    cursor.close()
    conn.close()
