from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import docker

app = FastAPI()

container_name = "nginx-container"

# Modelos Pydantic para validação dos dados de entrada
class CreateRuleRequest(BaseModel):
    server_name: str
    proxy_pass: str

class EditRuleRequest(BaseModel):
    proxy_pass: str

class InstallSSLRequest(BaseModel):
    domain: str
    email: str


@app.post("/api/rules", status_code=201)
async def create_rule(request: CreateRuleRequest):
    """
    Cria uma nova regra de proxy reverso no Nginx
    """
    try:
        # Cria o arquivo de configuração
        create_nginx_config(request.server_name, request.proxy_pass)
        # Reinicia o container Nginx
        restart_nginx_container(container_name)
        return {"message": "Regra criada com sucesso e Nginx reiniciado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/rules/{server_name}")
async def update_rule(server_name: str, request: EditRuleRequest):
    """
    Atualiza uma regra existente no Nginx
    """
    config_path = f'/etc/nginx/sites-available/{server_name}.conf'
    if not os.path.exists(config_path):
        raise HTTPException(status_code=404, detail="Regra não encontrada")
    
    try:
        # Sobrescreve a configuração existente
        create_nginx_config(server_name, request.proxy_pass)
        restart_nginx_container(container_name)
        return {"message": "Regra atualizada com sucesso e Nginx reiniciado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rules/{server_name}")
async def get_rule(server_name: str):
    """
    Obtém a configuração de uma regra específica
    """
    config_path = f'/etc/nginx/sites-available/{server_name}.conf'
    if not os.path.exists(config_path):
        raise HTTPException(status_code=404, detail="Regra não encontrada")
    
    try:
        with open(config_path, 'r') as f:
            config_content = f.read()
        return {
            "server_name": server_name,
            "config": config_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/rules/{server_name}")
async def delete_rule(server_name: str):
    """
    Remove uma regra do Nginx
    """
    config_path = f'/etc/nginx/sites-available/{server_name}.conf'
    enabled_path = f'/etc/nginx/sites-enabled/{server_name}.conf'
    
    try:
        # Remove link simbólico
        if os.path.exists(enabled_path):
            os.unlink(enabled_path)
        # Remove arquivo de configuração
        if os.path.exists(config_path):
            os.remove(config_path)
        # Reinicia o Nginx
        restart_nginx_container(container_name)
        return {"message": "Regra removida com sucesso e Nginx reiniciado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ssl")
async def install_ssl(request: InstallSSLRequest):
    """
    Instala certificado SSL usando Certbot
    """
    try:
        install_ssl_certificate(
            container_name=container_name,
            domain=request.domain,
            email=request.email
        )
        return {"message": "Certificado SSL instalado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
