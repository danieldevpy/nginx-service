from dataclasses import dataclass, field
from ..repositories.nginx_repository import NginxRepository
from ..repositories.server_renderer import ServerRenderer
from ..helpers.ssl_helper import SSLHelper
from ..models.server import Server


@dataclass
class ServerService:
    """
    Serviço responsável por gerenciar servidores Nginx.

    Este serviço atua como camada de orquestração entre os componentes:
    - **NginxRepository**: Repositório responsável por manipular arquivos de configuração do Nginx.
    - **ServerRenderer**: Renderizador que gera blocos de configuração a partir de objetos `Server`.
    - **SSLHelper**: Utilitário para detecção e preservação de regras SSL nos blocos de configuração.

    As responsabilidades do serviço incluem:
    - Criar, editar e excluir servidores.
    - Ativar e desativar servidores.
    - Garantir que configurações sejam válidas antes de persistir.
    - Preservar regras SSL existentes ao editar servidores.
    - Reiniciar o Nginx para aplicar alterações.
    """

    repo_nginx: NginxRepository
    repo_render: ServerRenderer
    ssl_helper: SSLHelper = field(default_factory=SSLHelper)

    def create_server(self, server: Server, default_active: bool = True) -> str:
        """
        Cria e salva um novo servidor no Nginx.

        Args:
            server (Server): Objeto que representa o servidor a ser criado.
            default_active (bool, opcional): Define se o servidor deve ser ativado imediatamente
                após ser criado. Padrão é True.

        Raises:
            ValueError: Se já existir um servidor com o mesmo nome.
            ValueError: Se a configuração renderizada for inválida.

        Returns:
            str: Bloco de configuração do servidor gerado e salvo.
        """
        if self.repo_nginx.server_exists(server.server_name):
            raise ValueError(f"Server '{server.server_name}' já existe!")

        block_config = self.repo_render.render(server)

        if not self.repo_nginx.validate_server_config(block_config):
            raise ValueError(f"Configuração inválida para o server '{server.server_name}'.")

        self.repo_nginx.save_server_config(server.server_name, block_config)
        if default_active:
            self.repo_nginx.enable_server(server.server_name)

        return block_config

    def edit_server(self, server_name: str, new_server: Server) -> str:
        """
        Edita um servidor existente, preservando regras SSL caso existam.

        Args:
            server_name (str): Nome do servidor a ser editado.
            new_server (Server): Novo objeto com as definições atualizadas do servidor.

        Raises:
            ValueError: Se o servidor não existir.
            ValueError: Se a nova configuração for inválida.

        Returns:
            str: Novo bloco de configuração renderizado e salvo.
        """
        if not self.repo_nginx.server_exists(server_name):
            raise ValueError(f"Server '{server_name}' não existe!")

        old_block = self.repo_nginx.get_server_config(server_name)

        ssl_rules = None
        if self.ssl_helper.check_has_ssl(old_block):
            _, ssl_rules = self.ssl_helper.edit_server_block(old_block)

        new_block = self.repo_render.render(new_server)

        if ssl_rules:
            new_block = self.ssl_helper.insert_rules_ssl(new_block, ssl_rules)

        if not self.repo_nginx.validate_server_config(new_block):
            raise ValueError(f"Nova configuração inválida para o server '{new_server.server_name}'.")

        if self.repo_nginx.is_server_enabled(server_name):
            self.repo_nginx.disable_server(server_name)

        self.repo_nginx.delete_server_config(server_name)
        self.repo_nginx.save_server_config(new_server.server_name, new_block)
        self.repo_nginx.enable_server(new_server.server_name)

        return new_block

    def delete_server(self, server_name: str) -> None:
        """
        Remove a configuração de um servidor do Nginx.

        Args:
            server_name (str): Nome do servidor a ser removido.

        Raises:
            ValueError: Se o servidor não existir.
        """
        if not self.repo_nginx.server_exists(server_name):
            raise ValueError(f"Server '{server_name}' não existe!")

        if self.repo_nginx.is_server_enabled(server_name):
            self.repo_nginx.disable_server(server_name)

        self.repo_nginx.delete_server_config(server_name)

    def enable_server(self, server_name: str) -> None:
        """
        Ativa um servidor no Nginx.

        Args:
            server_name (str): Nome do servidor a ser ativado.

        Raises:
            ValueError: Se o servidor já estiver habilitado.
        """
        if self.repo_nginx.is_server_enabled(server_name):
            raise ValueError(f"Server '{server_name}' já está habilitado!")
        self.repo_nginx.enable_server(server_name)

    def disable_server(self, server_name: str) -> None:
        """
        Desativa um servidor no Nginx.

        Args:
            server_name (str): Nome do servidor a ser desativado.

        Raises:
            ValueError: Se o servidor já estiver desabilitado.
        """
        if not self.repo_nginx.is_server_enabled(server_name):
            raise ValueError(f"Server '{server_name}' já está desabilitado!")
        self.repo_nginx.disable_server(server_name)

