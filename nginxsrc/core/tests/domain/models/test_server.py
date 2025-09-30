
from core.domain.models.server import Server

def test_default_server():
    default_server = Server(server_name="cisbaf.org.br")

    assert default_server.server_name == "cisbaf.org.br"
    assert default_server.listen == 80
    assert default_server.ssl == False
    assert len(default_server.extra_settings) == 0
    assert len(default_server.locations) == 0