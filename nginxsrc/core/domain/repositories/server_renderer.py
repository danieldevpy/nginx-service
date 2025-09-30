from abc import ABC, abstractmethod
from ..models.server import Server


class ServerRenderer(ABC):
    """
    Abstrai a geração do bloco de configuração do Nginx a partir de um Server.
    """

    @abstractmethod
    def render(self, server: Server) -> str:
        """
        Gera o bloco de configuração a partir do objeto Server.

        Args:
            server (Server): O modelo do servidor a ser renderizado.

        Returns:
            str: Bloco de configuração do Nginx.
        """
        pass