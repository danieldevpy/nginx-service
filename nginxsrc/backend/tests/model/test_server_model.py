from backend import ServerDTO, Server

def test_server_no_id():
    server = ServerDTO(id=1, server_name="teste").no_id()
    assert isinstance(server, Server)