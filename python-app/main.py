import os
import docker

def create_nginx_config(server_name, proxy_pass):
    """
    Cria um arquivo de configuração do Nginx e um link simbólico em sites-enabled.
    """
    config = f"""
    server {{
        listen 80;
        server_name {server_name};

        location / {{
            proxy_pass http://{proxy_pass};
        }}
    }}
    """

    # Caminho onde o arquivo será criado
    config_path = f'/etc/nginx/sites-available/{server_name}.conf'
    with open(config_path, 'w') as f:
        f.write(config)

    # Criar um link simbólico em sites-enabled
    enabled_path = f'/etc/nginx/sites-enabled/{server_name}.conf'
    if not os.path.exists(enabled_path):
        os.symlink(config_path, enabled_path)

    print(f"Configuração do Nginx criada para {server_name}.")

def install_ssl_certificate(container_name, domain, email):
    """
    Instala um certificado SSL usando o Certbot no container do Nginx.
    """
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        
        # Comando para instalar o certificado usando Certbot
        command = f"certbot --nginx -d {domain} --non-interactive --agree-tos --email {email}"
        
        # Executa o comando dentro do container
        exec_result = container.exec_run(command, stream=True)
        
        # Exibe a saída do comando em tempo real
        for line in exec_result.output:
            print(line.decode('utf-8').strip())
        
        if exec_result.exit_code == 0:
            print(f"Certificado SSL instalado com sucesso para o domínio: {domain}")
            restart_nginx_container(container_name)
        else:
            print(f"Erro ao instalar o certificado SSL. Código de saída: {exec_result.exit_code}")
    except Exception as e:
        print(f"Falha ao instalar o certificado SSL: {e}")

def restart_nginx_container(container_name):
    """
    Reinicia o container do Nginx para aplicar as mudanças.
    """
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        container.restart()
        print(f"Container Nginx '{container_name}' reiniciado com sucesso.")
    except Exception as e:
        print(f"Falha ao reiniciar o container: {e}")

