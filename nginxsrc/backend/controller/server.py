from typing import Optional
from dataclasses import dataclass, field
from ..model.server import Server, ServerDTO
from ..repositories.server_repository import ServerRepository
from .. import ServerService


@dataclass
class ServerController:
    server_repository: ServerRepository
    server_service: ServerService

    def create(self, server: Server):
        self.server_service.create_server(server)
        return self.server_repository.create(server)

    def get_all(self):
        return self.server_repository.get_all()

    def update(self, id: int, server: Server):
        server_dto = self.server_repository.get_by_id(id)
        if not server_dto:
            raise ValueError("Server não encontrado!")
        
        # atualizando no serviço nginx
        self.server_service.edit_server(
            server_name=server_dto.server_name,
            new_server=server
        )

        return self.server_repository.update(id, server)

    def delete(self, id: int):
        server_dto = self.server_repository.get_by_id(id)
        if not server_dto:
            raise ValueError("Server não encontrado!")
        
        self.server_service.delete_server(server_dto.server_name)
        
        return self.server_repository.delete(id)