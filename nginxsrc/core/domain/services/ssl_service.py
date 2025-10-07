from typing import Optional
from dataclasses import dataclass, field
from ..repositories.nginx_repository import NginxRepository
from ..repositories.ssl_repository import SSLRepository
from ..helpers.ssl_helper import SSLHelper

@dataclass
class SSLService:
    repo_nginx: NginxRepository
    repo_ssl: SSLRepository
    repo_helper: Optional[SSLHelper] = field(default_factory=SSLHelper)

    def install(self, server_name: str, email: str):
        if not self.repo_nginx.server_exists(server_name):
            raise ...
        
        ssl_info = self.repo_ssl.install(server_name, email)
        
        block = self.repo_nginx.get_server_config(server_name)

        if self.repo_helper.check_has_ssl(block):
            
            return ssl_info
        
        raise ...
        
    def uninstall(self):
        pass