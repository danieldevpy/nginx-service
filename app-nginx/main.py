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


def install_ssl_certificate(domain_name, certbot_container="certbot"):
    """Executa o Certbot para obter um certificado SSL."""
    client = docker.from_env()
    try:
        certbot_cmd = f"certbot certonly --webroot -w /var/www/certbot -d {domain_name} --non-interactive --agree-tos --email seu-email@dominio.com --rsa-key-size 4096 --force-renewal"
        container = client.containers.run("certbot/certbot", certbot_cmd, remove=True, volumes={
            "./nginx-content/certbot-etc": {"bind": "/etc/letsencrypt", "mode": "rw"},
            "./nginx-content/certbot-var": {"bind": "/var/lib/letsencrypt", "mode": "rw"},
            "./nginx-content/sites-enabled": {"bind": "/var/www/certbot", "mode": "rw"},
        }, detach=True)
        print(f"Certbot is running for {domain_name}")
        container.wait()
    except Exception as e:
        print(f"Failed to obtain SSL certificate: {e}")


