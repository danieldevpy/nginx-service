from core.domain.models.server import Server
from core.domain.models.location import Location
from core.domain.models.location_type import LocationType
from core.application.renders.jinja_renderer import JinjaServerRenderer

def test_jinja_renderer_proxy_block():
    renderer = JinjaServerRenderer()
    server = Server(
        server_name="example.com",
        ssl=True,
        locations=[
            Location(path="/", type=LocationType.PROXY, proxy_pass="http://127.0.0.1:3000")
        ]
    )

    block = renderer.render(server)

    assert "listen 80;" in block
    assert "server_name example.com;" in block
    assert "location /" in block
    assert "proxy_pass http://127.0.0.1:3000/;" in block
