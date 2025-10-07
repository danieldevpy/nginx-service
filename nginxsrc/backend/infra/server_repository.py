from dataclasses import dataclass
from sqlalchemy.engine import Engine
from sqlmodel import Session, select
from sqlmodel import SQLModel, Field, Column, Text, Session, select
# from ..repositories.server_repository import ServerRepository, ServerDTO
from ..repositories.server_repository import ServerRepository, ServerDTO
import json

class ServerData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    data: str = Field(sa_column=Column(Text, nullable=False))  # <- mover nullable para Column

@dataclass
class ServerSqlModel(ServerRepository):
    engine: Engine

    def _serializer(self, server_data: ServerData) -> ServerDTO:
        return ServerDTO(
            id=server_data.id,
            **json.loads(server_data.data)
        )

    def get_all(self):
        with Session(self.engine) as session:
            statement = select(ServerData)
            query = session.exec(statement)
            servers = [
                self._serializer(server_data)
                for server_data in query.all()
            ]
            return servers
    
    def get_by_id(self, id):
        with Session(self.engine) as session:
            server_data = session.get(ServerData, id)
            if server_data:
                return self._serializer(server_data)
            return None
    
    def create(self, server):
        server_json = server.model_dump_json()
        server_data = ServerData(data=server_json)
        with Session(self.engine) as session:
            session.add(server_data)
            session.commit()
            session.refresh(server_data)
            return self._serializer(server_data)
        
    def update(self, id, server):
        server_json = server.model_dump_json()
        with Session(self.engine) as session:
            server_data = session.get(ServerData, id)
            if not server_data:
                return None
            # atualizando 
            server_data.data = server_json
            session.add(server_data)
            session.commit()
            return self._serializer(server_data)
    
    def delete(self, id):
        with Session(self.engine) as session:
            server_data = session.get(ServerData, id)
            if not server_data:
                return False
            session.delete(server_data)
            session.commit()
            return True