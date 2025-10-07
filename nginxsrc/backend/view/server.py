from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from ..model.server import Server, ServerDTO
from ..controller.server import ServerController
from ..instances import InstancesRepository

controller = ServerController(
    server_repository=InstancesRepository().server_repository,
    server_service=InstancesRepository().server_service
)

router = APIRouter(
    prefix="/server",
    tags=["Server"]
)

@router.get(
    path="/",
    response_model=List[ServerDTO],
    summary="Lista todos os servidores"
)
def get_all_servers_endpoint():
    """Retorna todos os servidores cadastrados"""
    return controller.get_all()

@router.post(
    path="/",
    response_model=ServerDTO,
    summary="Cria um novo servidor"
)
def create_server_endpoint(server: Server):
    """Cria um novo servidor"""
    return controller.create(server)

@router.put(
    path="/{id}",
    response_model=ServerDTO,
    summary="Edita um servidor existente"
)
def edit_server_endpoint(
    id: int,
    server: Server
):
    """Edita um servidor pelo ID"""
    return controller.update(id, server)
    # server_dto = crud.get_server_by_id(id)
    # if not server_dto:
    #     raise HTTPException(status_code=404, detail="Server não encontrado!")
    # repositories.server.edit_server(server_dto.server_name, server)
    # updated = crud.update_server(server_dto.id, server)
    # if updated:
    #     return updated
    # raise HTTPException(status_code=500, detail="Erro ao atualizar o servidor")

@router.delete(
    path="/{id}",
    summary="Deleta um servidor pelo ID"
)
def delete_server_endpoint(id: int):
    """Deleta um servidor pelo ID"""
    return controller.delete(id)