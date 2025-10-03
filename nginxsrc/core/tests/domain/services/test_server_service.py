import pytest
from core import  Server, Location

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

def test_create_server_success(server_service, server_instance):
    service, repo_nginx = server_service
    block = service.create_server(server_instance)
    assert repo_nginx.get_server_config(server_instance.server_name) == block
    assert repo_nginx.is_server_enabled(server_instance.server_name) == True

def test_create_server_already_exists(server_service, server_instance):
    service, _ = server_service
    service.create_server(server_instance)
    with pytest.raises(ValueError, match="já existe"):
        service.create_server(server_instance)


def test_edit_server_success(server_service, server_instance):
    service, repo_nginx = server_service
    service.create_server(server_instance)

    server_instance.locations.append(
        Location(path="/to", type="redirect", redirect_to="http://localhost:8001", status_code=301)
    )
    
    block = service.edit_server(server_instance.server_name, server_instance)

    assert "location /to" in block
    assert "return 301 http://localhost:8001/" in block
    assert repo_nginx.get_server_config(server_instance.server_name) == block

def test_edit_server_not_exists(server_service, server_instance):
    service, _ = server_service
    with pytest.raises(ValueError, match="não existe"):
        service.edit_server("naoexiste.com", server_instance)

def test_change_server_name(server_service, server_instance):
    service, repo_nginx = server_service
    service.create_server(server_instance)

    old_name = server_instance.server_name
    server_instance.server_name = "cisbaf.com.br"
    service.edit_server(old_name, server_instance)

    assert repo_nginx.get_server_config("cisbaf.com.br")
    with pytest.raises(Exception, match=old_name):
        repo_nginx.get_server_config(old_name)

def test_delete_server_success(server_service, server_instance):
    service, repo_nginx = server_service
    service.create_server(server_instance)
    service.delete_server(server_instance.server_name)
    with pytest.raises(Exception, match="does not exist"):
        repo_nginx.get_server_config(server_instance.server_name)

def test_delete_server_not_exists(server_service):
    service, _ = server_service
    with pytest.raises(ValueError, match="não existe"):
        service.delete_server("naoexiste.com")

def test_enable_server_success(server_service, server_instance):
    service, repo_nginx = server_service
    service.create_server(server_instance, False)
    service.enable_server(server_instance.server_name)
    assert repo_nginx.is_server_enabled(server_instance.server_name) is True

def test_enable_server_already_enabled(server_service, server_instance):
    service, _ = server_service
    service.create_server(server_instance)
    with pytest.raises(ValueError, match="já está habilitado"):
        service.enable_server(server_instance.server_name)

def test_disable_server_success(server_service, server_instance):
    service, repo_nginx = server_service
    service.create_server(server_instance)
    service.disable_server(server_instance.server_name)
    assert repo_nginx.is_server_enabled(server_instance.server_name) is False

def test_disable_server_already_disabled(server_service, server_instance):
    service, _ = server_service
    service.create_server(server_instance, False)
    with pytest.raises(ValueError, match="já está desabilitado"):
        service.disable_server(server_instance.server_name)