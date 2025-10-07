# tests/conftest.py
import pytest
from backend import create_engine_instance, create_tables,ServerSqlModel

@pytest.fixture(name="test_engine")
def test_engine_fixture():
    engine = create_engine_instance("sqlite:///:memory:")
    create_tables(engine)
    yield engine
    engine.dispose()

@pytest.fixture(name="repo")
def repo_fixture(test_engine):
    return ServerSqlModel(engine=test_engine)
