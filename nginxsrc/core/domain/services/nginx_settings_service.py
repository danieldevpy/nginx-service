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