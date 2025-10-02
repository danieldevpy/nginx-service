from typing import Optional, List
from sqlmodel import Session, select
from .models import engine, ServerData, ServerDTO
from ..core.domain.models.server import Server
import json

def create_server_data(server: Server) -> ServerDTO:
    with Session(engine) as session:
        db_server = ServerData(data=server.model_dump_json())
        session.add(db_server)
        session.commit()
        session.refresh(db_server)
        return ServerDTO(
            id=db_server.id,
            **json.loads(db_server.data)
        )

# Read por ID
def get_server_by_id(server_id: int) -> Optional[ServerDTO]:
    with Session(engine) as session:
        db_server = session.get(ServerData, server_id)
        if db_server:
            return ServerDTO(
                id=db_server.id,
                **json.loads(db_server.data)
            ) 
        return None

# Read all
def get_all_servers() -> List[ServerDTO]:
    with Session(engine) as session:
        db_servers = session.exec(select(ServerData)).all()
        servers_dto = [
            ServerDTO(
                id=db_server.id,
                **json.loads(db_server.data)
            ) 
            for db_server in db_servers]
        return servers_dto

# Update
def update_server(server_id: int, server: Server) -> Optional[ServerDTO]:
    with Session(engine) as session:
        db_server = session.get(ServerData, server_id)
        if not db_server:
            return None
        db_server.data = server.model_dump_json()
        session.add(db_server)
        session.commit()
        session.refresh(db_server)
        return ServerDTO(
            id=db_server.id,
            **json.loads(db_server.data)
        ) 

# Delete
def delete_server(server_id: int) -> bool:
    with Session(engine) as session:
        db_server = session.get(ServerData, server_id)
        if not db_server:
            return False
        session.delete(db_server)
        session.commit()
        return True