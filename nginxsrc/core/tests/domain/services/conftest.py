import pytest
from core.application.renders.jinja_renderer import JinjaServerRenderer
from core.application.memory.in_memory_nginx_repository import InMemoryNginxRepository
from core import ServerService

@pytest.fixture
def server_service():
    repo_nginx = InMemoryNginxRepository()
    repo_jinja = JinjaServerRenderer()
    return ServerService(repo_nginx, repo_jinja), repo_nginx