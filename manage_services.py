import subprocess

def stop_grafana_service():
    try:
        print("Stopping Grafana service...")
        subprocess.run(["sudo", "systemctl", "stop", "grafana-server"], check=True)
        print("Grafana service stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop Grafana service: {e}")

def build_nmap_image():
    try:
        print("Building Nmap Docker image...")
        subprocess.run(["docker-compose", "build", "--no-cache", "nmap"], check=True)
        print("Nmap Docker image built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to build Nmap Docker image: {e}")

def restart_docker_compose():
    try:
        print("Restarting Docker Compose services...")
        subprocess.run(["docker-compose", "up", "-d", "--force-recreate"], check=True)
        print("Docker Compose services restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart Docker Compose services: {e}")

def start_grafana_service():
    try:
        print("Starting Grafana service...")
        subprocess.run(["sudo", "systemctl", "start", "grafana-server"], check=True)
        print("Grafana service started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Grafana service: {e}")

def main():
    #stop_grafana_service()
    build_nmap_image()
    restart_docker_compose()
    #start_grafana_service()

if __name__ == "__main__":
    main()
