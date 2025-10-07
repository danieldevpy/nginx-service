from core.domain.models.server import Server

def test_default_server():
    default_server = Server(server_name="cisbaf.org.br")

    assert default_server.server_name == "cisbaf.org.br"
    assert default_server.listen == 80
    assert default_server.ssl.active == False
    assert default_server.ssl.expiry == None
    assert default_server.extra_settings == None
    assert len(default_server.locations) == 0