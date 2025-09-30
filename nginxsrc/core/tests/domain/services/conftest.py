import pytest
from core.application.renders.jinja_renderer import JinjaServerRenderer
from core.application.memory.in_memory_nginx_repository import InMemoryNginxRepository
from core import NginxService

@pytest.fixture
def nginx_service():
    repo_nginx = InMemoryNginxRepository()
    repo_jinja = JinjaServerRenderer()
    return NginxService(repo_nginx, repo_jinja), repo_nginx