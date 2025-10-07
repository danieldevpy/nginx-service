import pytest
from core.application.memory.in_memory_ssl_repository import InMemorySSL
from core.application.renders.jinja_renderer import JinjaServerRenderer
from core.application.memory.in_memory_nginx_repository import InMemoryNginxRepository
from core import ServerService, SSLService


@pytest.fixture
def server_service():
    repo_nginx = InMemoryNginxRepository()
    repo_jinja = JinjaServerRenderer()
    return ServerService(repo_nginx, repo_jinja), repo_nginx

@pytest.fixture
def ssl_service():
    def wrapper(repo_nginx):
        ssl_repo = InMemorySSL(repo_nginx)
        return SSLService(repo_nginx, ssl_repo)
    return wrapper