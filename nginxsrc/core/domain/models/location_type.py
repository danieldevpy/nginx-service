from enum import Enum

class LocationType(str, Enum):
    """
    Enum que representa os tipos de Location suportados no Nginx.

    Tipos:
        PROXY       : Proxy reverso.
        REDIRECT    : Redirecionamento HTTP.
        STATIC      : Conteúdo estático.
        REWRITE     : Reescrita de URL.
        MAINTENANCE : Página em manutenção
    """
    PROXY = "proxy"
    REDIRECT = "redirect"
    STATIC = "static"
    REWRITE = "rewrite"
    MAINTENANCE = "maintenance"
