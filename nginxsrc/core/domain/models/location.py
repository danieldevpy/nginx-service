from pydantic import BaseModel, model_validator
from typing import Optional
from ..helpers.http_url import PreservedHttpUrl
from .location_type import LocationType

class Location(BaseModel):
    """
    Entidade que representa uma 'location' dentro de um servidor Nginx.

    Dependendo do tipo de Location (LocationType), campos diferentes são obrigatórios:

        - PROXY: proxy_pass
        - REDIRECT: redirect_to, status_code
        - STATIC: root
        - REWRITE: rewrite_rule
    """

    path: str
    """Caminho da location (ex: /api, /static)."""

    type: LocationType
    """Tipo da location (proxy, redirect, static, rewrite)."""

    active: Optional[bool] = True
    """Se False a location não deverá ser escrita!"""

    # Proxy reverso
    proxy_pass: Optional[PreservedHttpUrl] = None
    """URL do proxy reverso (obrigatório se type=proxy)."""

    # Redirect
    redirect_to: Optional[PreservedHttpUrl] = None
    """URL de destino do redirecionamento (obrigatório se type=redirect)."""
    status_code: Optional[int] = None
    """Código HTTP do redirecionamento (obrigatório se type=redirect)."""

    # Estático
    root: Optional[str] = None
    """Caminho do diretório raiz para servir arquivos estáticos (obrigatório se type=static)."""

    # Rewrite
    rewrite_rule: Optional[str] = None
    """Expressão de reescrita da URL (obrigatório se type=rewrite)."""
    last: Optional[bool] = None
    """Se a reescrita deve usar a flag 'last'."""

    @model_validator(mode="after")
    def validate_required_fields(self):
        """
        Valida os campos obrigatórios de acordo com o tipo da location.
        Levanta ValueError se algum campo necessário estiver ausente.
        """
        required_fields = {
            LocationType.PROXY: ["proxy_pass"],
            LocationType.REDIRECT: ["redirect_to", "status_code"],
            LocationType.STATIC: ["root"],
            LocationType.REWRITE: ["rewrite_rule"],
        }

        missing = [
            field for field in required_fields.get(self.type, [])
            if getattr(self, field) is None
        ]

        if missing:
            raise ValueError(
                f"Para type='{self.type}' os campos obrigatórios são: {', '.join(missing)}"
            )

        return self
