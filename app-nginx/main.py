import os
import docker

def create_nginx_config(server_name, proxy_pass):
    config = f"""
    server {{
        listen 80;
        server_name {server_name};

        location / {{
            return 301 http://google.com;
        }}
    }}
    """

    # Caminho onde o arquivo será criado
    config_path = '/etc/nginx/sites-available/{}.conf'.format(server_name)
    with open(config_path, 'w') as f:
        f.write(config)

    # Criar um link simbólico em sites-enabled
    enabled_path = '/etc/nginx/sites-enabled/{}.conf'.format(server_name)
    if not os.path.exists(enabled_path):
        os.symlink(config_path, enabled_path)

def restart_nginx_container(container_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        container.restart()
        print(f"Nginx container '{container_name}' restarted successfully.")
    except Exception as e:
        print(f"Failed to restart container: {e}")

if __name__ == "__main__":
    create_nginx_config('localhost', 'http://google.com')
    restart_nginx_container('nginxservice-nginx-container-1')  # Substitua 'nginx' pelo nome do seu container
