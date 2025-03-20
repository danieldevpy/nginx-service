import os
import docker
from config import settings
from typing import List

def make_path(paths: List[str]):
    return os.path.join(**paths)

def create_nginx_config(server_name, proxy_pass):
    config = f"""
    server {{
        listen 80;
        server_name {server_name};

        location / {{
            proxy_pass http://{proxy_pass};
        }}
    }}
    """
    config_path = f'/etc/nginx/sites-available/{server_name}.conf'
    with open(config_path, 'w') as f:
        f.write(config)

    enabled_path = f'/etc/nginx/sites-enabled/{server_name}.conf'
    if not os.path.exists(enabled_path):
        os.symlink(config_path, enabled_path)

def restart_nginx_container():
    client = docker.from_env()
    try:
        container = client.containers.get(settings.NGINX_CONTAINER_NAME)
        container.restart()
    except Exception as e:
        raise Exception(f"Falha ao reiniciar o container: {e}")

def install_ssl_certificate(domain, email):
    client = docker.from_env()
    try:
        container = client.containers.get(settings.NGINX_CONTAINER_NAME)
        command = f"certbot --nginx -d {domain} --non-interactive --agree-tos --email {email}"
        exec_result = container.exec_run(command, stream=True)
        
        for line in exec_result.output:
            print(line.decode('utf-8').strip())
        
        if exec_result.exit_code == 0:
            restart_nginx_container()
        else:
            raise Exception(f"Erro ao instalar o certificado SSL. Código de saída: {exec_result.exit_code}")
    except Exception as e:
        raise Exception(f"Falha ao instalar o certificado SSL: {e}")
    
import docker
import os

def validate_nginx_config(config_content):
    temp_config_path = '/tmp/nginx_temp.conf'
    with open(temp_config_path, 'w') as f:
        f.write(f'''
        events {{}}
        http {{
            {config_content}
        }}
        ''')
    
    try:
        client = docker.from_env()
        container = client.containers.get(settings.NGINX_CONTAINER_NAME)
        
        # Executa o comando de teste do Nginx sem stream
        exec_result = container.exec_run(f"nginx -t -c {temp_config_path}", stream=False)
        
        # Decodifica a saída
        output = exec_result.output.decode('utf-8').strip()
        
        # Verifica o código de saída
        if exec_result.exit_code != 0:
            raise Exception("Configuração do Nginx inválida:", str(output))
        
        print("Configuração do Nginx válida.")
    except Exception as e:
        print(f"Erro ao validar configuração do Nginx: {e}")
        raise
    finally:
        # Remove o arquivo temporário
        if os.path.exists(temp_config_path):
            os.remove(temp_config_path)