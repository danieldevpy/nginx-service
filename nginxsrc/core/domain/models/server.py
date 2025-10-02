from pydantic import BaseModel, Field
from typing import List, Optional
from .location import Location
from .setting import Settings


class Server(BaseModel):
    """
    Representa um servidor Nginx com suas configurações básicas e rotas (locations).
    """

    server_name: str = Field(
        ...,
        description="Nome do servidor (ex: domínio ou identificador interno).",
    )

    listen: Optional[int] = Field(
        80,
        description="Porta na qual o servidor vai escutar. Padrão é 80."
    )

    extra_settings: Optional[Settings] = Field(
        None,
        description="Inserir configurações extras. Como 'client_max_body_size'",
    )

    ssl: Optional[bool] = Field(
        False,
        description="Indica se o servidor utiliza SSL/TLS. Padrão é False."
    )

    locations: List[Location] = Field(
        default_factory=list,
        description="Lista de locations configuradas neste servidor."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "server_name": "meu-dominio.com",
                "listen": 80,
                "locations": [
                    {"path": "/", "type": "proxy", "proxy_pass": "https://example.com/"}
                ]
            }
        }
    }