from typing import Protocol, List


class NginxRepository(Protocol):
    """
    Interface para manipulação de arquivos de configuração do Nginx e do Serviço.
    """

    def start_service(self) -> None:
        """
        Inicia o serviço Nginx.
        """
        ...

    def stop_service(self) -> None:
        """
        Para o serviço Nginx.
        """
        ...

    def restart_service(self) -> None:
        """
        Reinicia o serviço do Nginx para aplicar alterações nas configurações.
        """
        ...

    def get_servers_name(self) -> List[str]:
        """
        Retorna uma lista com os nomes dos servidores configurados no Nginx.

        Cada nome da lista corresponde a um 'server_name' definido
        nos blocos de servidor (server blocks) dos arquivos de configuração
        do Nginx.

        Retornos:
            List[str]: Uma lista de strings, cada uma representando o nome
            de um servidor configurado no Nginx. Se nenhum servidor estiver
            configurado, a lista será vazia.

        Exemplo de uso:
            >>> nginx_repo.get_servers_name()
            ['example.com', 'api.example.com', 'localhost']
        """
        ...

    def server_exists(self, server_name: str) -> bool:
        """
        Verifica se um servidor com o nome fornecido já existe.
        
        Args:
            server_name (str): Nome do servidor.
            
        Returns:
            bool: True se o servidor existir, False caso contrário.
        """
        ...

    def get_server_config(self, server_name: str) -> str:
        """
        Retorna o conteúdo da configuração de um servidor específico.
        
        Args:
            server_name (str): Nome do servidor.
            
        Returns:
            str: Conteúdo da configuração do servidor.
        """
        ...

    def save_server_config(self, server_name: str, content: str) -> None:
        """
        Cria ou atualiza a configuração de um servidor no Nginx.
        
        Args:
            server_name (str): Nome do servidor.
            content (str): Conteúdo da configuração a ser salva.
        """
        ...

    def delete_server_config(self, server_name: str) -> None:
        """
        Remove a configuração de um servidor do Nginx.
        
        Args:
            server_name (str): Nome do servidor a ser removido.
        """
        ...

    def enable_server(self, server_name: str) -> None:
        """
        Ativa a configuração de um servidor no Nginx (ex.: criando symlink em sites-enabled).
        
        Args:
            server_name (str): Nome do servidor a ser ativado.
        """
        ...

    def disable_server(self, server_name: str) -> None:
        """
        Desativa a configuração de um servidor no Nginx (ex.: removendo symlink em sites-enabled).
        
        Args:
            server_name (str): Nome do servidor a ser desativado.
        """
        ...

    def validate_server_config(self, content: str) -> bool:
        """
        Valida a sintaxe de um arquivo de configuração de servidor do Nginx.
        
        Args:
            content (str): Conteúdo da configuração a ser validada.
        
        Returns:
            bool: True se a configuração for válida, False caso contrário.
        """
        ...
        
    def is_server_enabled(self, server_name: str) -> bool:
        """
        Verifica se a configuração de um servidor está ativa (habilitada).
        
        Args:
            server_name (str): Nome do servidor.
        
        Returns:
            bool: True se o servidor estiver habilitado, False caso contrário.
        """
        ...

    def get_status(self) -> str:
        """
        Retorna o status do serviço Nginx, especificamente a linha 'Active:'.
        """
        ...