from ...domain.repositories.nginx_repository import NginxRepository
from ...domain.repositories.ssl_repository import SSLRepository
from ...domain.helpers.ssl_helper import SSLHelper
from ...domain.models.ssl import SSL
from datetime import datetime, timedelta
from dataclasses import dataclass

def block_server():
    return """
    server {
        server_name chamadosti.cisbaf.org.br;

        access_log /var/log/nginx/(chamadosti.cisbaf.org.br)_access.log;
        error_log /var/log/nginx/(chamadosti.cisbaf.org.br)_error.log;

        location / {
            include /etc/nginx/proxy_settings.conf;
            proxy_pass http://192.168.1.10:8000;
        }
	# end
    
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/chamadosti.cisbaf.org.br/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/chamadosti.cisbaf.org.br/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}
"""

@dataclass
class InMemorySSL(SSLRepository):
    repo_nginx: NginxRepository

    def install(self, server_name, email) -> SSL:
        helper = SSLHelper()
        _, copy = helper.edit_server_block(block_server())
        block = self.repo_nginx.get_server_config(server_name)
        new_block = helper.insert_rules_ssl(block, copy)
        self.repo_nginx.save_server_config(server_name, new_block)

        return SSL(active=True, expiry=datetime.now() + timedelta(days=30), email=email)
  
    
    def uninstall(self, server_name):
        return super().uninstall(server_name)
    
    def info(self, server_name):
        return super().info(server_name)