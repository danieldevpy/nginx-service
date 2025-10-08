from jinja2 import Template
from ...domain.models.server import Server
from ...domain.repositories.server_renderer import ServerRenderer

class JinjaServerRenderer(ServerRenderer):
    TEMPLATE = """
server {
    server_name {{ server.server_name }};
    listen {{ server.listen }};

    {%- for line in server.extra_settings %}
    {{ line }};
    {%- endfor %}

    {% for loc in server.locations %}
        {%- if loc.active %}
    location {{ loc.path }} {
        {%- if loc.type.value == 'proxy' %}
        proxy_pass {{ loc.proxy_pass }};
        {%- elif loc.type.value == 'redirect' %}
        return {{ loc.status_code }} {{ loc.redirect_to }};
        {%- elif loc.type.value == 'static' %}
        root {{ loc.root }};
        {%- elif loc.type.value == 'rewrite' %}
        rewrite {{ loc.rewrite_rule }} {% if loc.last %}last{% endif %};
        {%- elif loc.type.value == 'maintenance' %}
        default_type text/html;
        return 200 '<h1>Manutencao</h1><p>Voltamos em breve.</p>';
        {%- endif %}
    }
        {%- endif %}
    {% endfor %}
    # end
}

"""

    def render(self, server: Server) -> str:
        template = Template(self.TEMPLATE)
        return template.render(server=server)
