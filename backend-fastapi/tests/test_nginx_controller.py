from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_rule():
    response = client.post(
        "/api/rules",
        json={"server_name": "test.com", "proxy_pass": "http://backend"}
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Regra criada com sucesso e Nginx reiniciado"}

def test_update_rule():
    response = client.put(
        "/api/rules/test.com",
        json={"proxy_pass": "http://new_backend"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Regra atualizada com sucesso e Nginx reiniciado"}

def test_get_rule():
    response = client.get("/api/rules/test.com")
    assert response.status_code == 200
    assert "config" in response.json()

def test_delete_rule():
    response = client.delete("/api/rules/test.com")
    assert response.status_code == 200
    assert response.json() == {"message": "Regra removida com sucesso e Nginx reiniciado"}

def test_install_ssl():
    response = client.post(
        "/api/ssl",
        json={"domain": "test.com", "email": "admin@test.com"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Certificado SSL instalado com sucesso"}