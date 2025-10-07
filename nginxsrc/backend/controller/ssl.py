from dataclasses import dataclass
from .. import SSLService
from ..repositories.server_repository import ServerRepository


@dataclass
class SSLController:
    server_repository: ServerRepository
    ssl_service: SSLService

    def install(self, id: int, email: str):
        server_dto = self.server_repository.get_by_id(id)
        if not server_dto:
            raise ValueError("Server não encontrado!")
        
        if server_dto.ssl.active:
            raise ValueError("O SSL já está ativo!")
        
        ssl_model = self.ssl_service.install(
            server_name=server_dto.server_name,
            email=email
        )

        # atualizando informações do ssl
        server_dto.ssl = ssl_model

        # atualizando no banco e obtendo novo objeto
        server_dto = self.server_repository.update(server_dto.id, server_dto.no_id())

        return server_dto