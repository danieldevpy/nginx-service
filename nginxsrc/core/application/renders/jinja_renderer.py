from jinja2 import Template
from ...domain.models.server import Server
from ...domain.repositories.server_renderer import ServerRenderer

# remove {% if server.ssl %} ssl{% endif %} do listen

class JinjaServerRenderer(ServerRenderer):
    TEMPLATE = """
server {
    listen {{ server.listen }};
    server_name {{ server.server_name }};

    {% for loc in server.locations %}
    location {{ loc.path }} {
        {% if loc.type.value == 'proxy' %}
        proxy_pass {{ loc.proxy_pass }};
        {% elif loc.type.value == 'redirect' %}
        return {{ loc.status_code }} {{ loc.redirect_to }};
        {% elif loc.type.value == 'static' %}
        root {{ loc.root }};
        {% elif loc.type.value == 'rewrite' %}
        rewrite {{ loc.rewrite_rule }} {% if loc.last %}last{% endif %};
        {% endif %}
    }
    {% endfor %}

    # end
}
"""

    def render(self, server: Server) -> str:
        template = Template(self.TEMPLATE)
        return template.render(server=server)
