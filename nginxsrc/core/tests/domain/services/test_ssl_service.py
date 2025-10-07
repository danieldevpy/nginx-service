import pytest
from core import Server, Location
from datetime import datetime


def test_install_ssl(server_service, ssl_service, server_instance):
    server_service, repo_nginx = server_service

    server_service.create_server(server_instance)
    ssl_service = ssl_service(repo_nginx)
    ssl_info = ssl_service.install(server_instance.server_name, "danielfernandes202@gmail.com")

    block = repo_nginx.get_server_config(server_instance.server_name)

    assert ssl_info.active == True
    assert ssl_info.expiry > datetime.now()
    assert ssl_info.email == "danielfernandes202@gmail.com"
    assert 'listen 443 ssl' in block
    assert 'ssl_certificate' in block
    assert 'ssl_certificate_key' in block
    assert 'include /etc/letsencrypt' in block
    assert 'ssl_dhparam' in block
    

@pytest.fixture
def server_instance():
    return Server(
        server_name="cisbaf.org.br",
        locations=[
            Location(
                path="/",
                type="proxy",
                proxy_pass="http://localhost:8000"
            )
        ]
    )