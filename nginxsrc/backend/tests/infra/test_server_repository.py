from backend import ServerSqlModel, Server, ServerDTO, ServerData
import json


def test_create_server(repo: ServerSqlModel):
    server = Server(server_name="google.com")
    dto = repo.create(server)
    assert dto.id == 1
    assert dto.server_name == "google.com"

def test_get_by_id(repo: ServerSqlModel):
    server = Server(server_name="server2.com")
    created = repo.create(server)

    result = repo.get_by_id(created.id)
    assert result is not None
    assert result.server_name == "server2.com"

def test_get_all(repo: ServerSqlModel):
    server1 = Server(server_name="s1.com")
    server2 = Server(server_name="s2.com")
    repo.create(server1)
    repo.create(server2)

    all_servers = repo.get_all()
    assert len(all_servers) == 2
    names = [s.server_name for s in all_servers]
    assert "s1.com" in names
    assert "s2.com" in names

def test_update_server(repo: ServerSqlModel):
    server = Server(server_name="old.com")
    created = repo.create(server)

    updated_server = Server(server_name="new.com")
    updated = repo.update(created.id, updated_server)

    assert updated.server_name == "new.com"
    assert repo.get_by_id(created.id).server_name == "new.com"

def test_delete_server(repo: ServerSqlModel):
    server = Server(server_name="delete.com")
    created = repo.create(server)

    deleted = repo.delete(created.id)
    assert deleted is True
    assert repo.get_by_id(created.id) is None

def test_delete_nonexistent_server(repo: ServerSqlModel):
    deleted = repo.delete(999)
    assert deleted is False

def test_update_nonexistent_server(repo: ServerSqlModel):
    fake_server = Server(server_name="fake.com")
    result = repo.update(999, fake_server)
    assert result is None


def test_serializer(repo: ServerSqlModel):
    # Cria um ServerData manualmente
    data_dict = {"server_name": "meu-servidor.com", "listen": 8080, "locations": []}
    server_data = ServerData(id=1, data=json.dumps(data_dict))

    # Chama _serializer
    dto = repo._serializer(server_data)

    assert isinstance(dto, ServerDTO)
    assert dto.id == 1
    assert dto.server_name == "meu-servidor.com"
    assert dto.listen == 8080
    assert dto.locations == []