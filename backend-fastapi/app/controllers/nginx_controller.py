from fastapi import APIRouter, HTTPException
from models.schemas import (
    CreateRuleRequest,
    EditRuleRequest,
    InstallSSLRequest,
    UpdateFullRuleRequest,
)
from services.nginx_service import NginxService

router = APIRouter()

@router.get("/api/rules", tags=["Rules"])
async def get_rules():
    """
    Retorna todas as regras de configuração do Nginx.

    Esta rota retorna uma lista de todas as regras de configuração atualmente
    armazenadas no serviço Nginx.

    **Exemplo de resposta:**
    - Código HTTP: 200
    - Corpo: Lista de regras de configuração em formato JSON
    """
    return NginxService.get_rules()

@router.get("/api/rules/{server_name}", tags=["Rules"])
async def get_rule(server_name: str):
    """
    Retorna uma regra de configuração do Nginx para um servidor específico.

    Esta rota retorna a configuração de proxy de um servidor específico baseado
    no `server_name` fornecido.

    - **server_name**: Nome do servidor (domínio) que deseja obter a configuração.

    **Exemplo de resposta:**
    - Código HTTP: 200
    - Corpo: Regra de configuração do servidor
    """
    return NginxService.get_rule(server_name)

@router.post("/api/rules", status_code=201, tags=["Rules"])
async def create_rule(request: CreateRuleRequest):
    """
    Cria uma nova regra de configuração no Nginx.

    Esta rota cria uma nova regra de proxy pass para o servidor com base no
    `server_name` e `proxy_pass` fornecidos.

    - **server_name**: Nome do servidor para o qual a configuração será aplicada.
    - **proxy_pass**: URL para o qual as requisições serão redirecionadas.

    **Exemplo de resposta:**
    - Código HTTP: 201
    - Corpo: Confirmação da criação da regra
    """
    return NginxService.create_rule(request.server_name, request.proxy_pass)

@router.post("/api/ssl", tags=["SSL"])
async def install_ssl(request: InstallSSLRequest):
    """
    Instala um certificado SSL para um domínio.

    Esta rota configura o SSL para um domínio, utilizando o `domain` e o
    `email` fornecidos.

    - **domain**: O domínio para o qual o SSL será configurado.
    - **email**: O e-mail associado à solicitação de SSL.

    **Exemplo de resposta:**
    - Código HTTP: 200
    - Corpo: Confirmação da instalação do SSL
    """
    return NginxService.install_ssl(request.domain, request.email)

@router.put("/api/rules/{server_name}", tags=["Rules"])
async def update_rule(server_name: str, request: EditRuleRequest):
    """
    Atualiza a configuração de proxy pass de uma regra existente.

    Esta rota permite atualizar a configuração de proxy de uma regra já existente
    com base no `server_name` e `proxy_pass` fornecidos.

    - **server_name**: Nome do servidor cuja configuração será atualizada.
    - **proxy_pass**: Nova URL de proxy pass para o servidor.

    **Exemplo de resposta:**
    - Código HTTP: 200
    - Corpo: Confirmação da atualização da regra
    """
    return NginxService.update_rule(server_name, request.proxy_pass)

@router.put("/api/rules/{server_name}/full", tags=["Rules"])
async def update_full_rule(server_name: str, request: UpdateFullRuleRequest):
    """
    Atualiza completamente a configuração de uma regra existente.

    Esta rota permite atualizar completamente a configuração de uma regra
    para um servidor específico com base no `server_name` e a configuração
    fornecida.

    - **server_name**: Nome do servidor cuja configuração será completamente atualizada.
    - **config**: A nova configuração completa para o servidor.

    **Exemplo de resposta:**
    - Código HTTP: 200
    - Corpo: Confirmação da atualização completa da regra
    """
    return NginxService.update_full_rule(server_name, request.config)

@router.delete("/api/rules/{server_name}", tags=["Rules"])
async def delete_rule(server_name: str):
    """
    Exclui uma regra de configuração do Nginx para um servidor específico.

    Esta rota remove a configuração de um servidor baseado no `server_name`
    fornecido.

    - **server_name**: Nome do servidor cuja configuração será excluída.

    **Exemplo de resposta:**
    - Código HTTP: 200
    - Corpo: Confirmação da exclusão da regra
    """
    return NginxService.delete_rule(server_name)
