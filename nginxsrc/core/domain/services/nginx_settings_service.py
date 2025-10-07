from dataclasses import dataclass
from ..repositories.nginx_repository import NginxRepository

@dataclass
class NginxSettingsService:
    repo_nginx: NginxRepository

    def get_status(self):
        """
        Retorna o status do serviço Nginx, especificamente a linha 'Active:'.
        """
        return self.repo_nginx.get_status()

    def reload(self) -> None:
        """
        Reinicia o serviço do Nginx para aplicar as alterações em produção.
        """
        self.repo_nginx.restart_service()

    def clean_servers(self) -> None:
        """"""
        servers_name = self.repo_nginx.get_servers_name()
        for server_name in servers_name:
            if self.repo_nginx.is_server_enabled(server_name):
                self.repo_nginx.disable_server(server_name)
            self.repo_nginx.delete_server_config(server_name)
            