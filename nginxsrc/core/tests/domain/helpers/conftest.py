import pytest

@pytest.fixture
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
    

    server {
    if ($host = chamadosti.cisbaf.org.br) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


        listen 80;
        server_name chamadosti.cisbaf.org.br;
    return 404; # managed by Certbot


}

    """