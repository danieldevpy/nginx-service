from core import NginxService, JinjaServerRenderer, NginxRepositoryLinux, Server, Location

server = Server(
    server_name="todolist.test",
    locations=[
        Location(
            path="/",
            type="proxy",
            proxy_pass="https://facebook.com",
            status_code=301
        )
    ]
)

service = NginxService(
    repo_nginx=NginxRepositoryLinux(sudo_password="devpython"),
    repo_render=JinjaServerRenderer()
)
service.edit_server(server.server_name, server)
service.reload()