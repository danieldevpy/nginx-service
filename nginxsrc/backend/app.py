from fastapi import FastAPI, Body, Request
from fastapi.responses import JSONResponse
from typing import List
from .models import ServerDTO, Server
from ..core import NginxService, JinjaServerRenderer, NginxRepositoryLinux
from ..backend import crud

app = FastAPI(title="API de Servidores")

service = NginxService(
    repo_nginx=NginxRepositoryLinux(sudo_password="devpython"),
    repo_render=JinjaServerRenderer()
)

@app.get("/", response_model=List[ServerDTO])
def get_all_servers_endpoint():
    return crud.get_all_servers()

@app.post("/", response_model=ServerDTO)
def create_server_endpoint(server: Server):
    service.create_server(server)
    service.reload()
    server_dto = crud.create_server_data(server)
    return server_dto

@app.put("/", response_model=ServerDTO)
def edit_server_endpoint(id: int, server: Server):
    server_dto = crud.get_server_by_id(id)
    if server_dto:
        service.edit_server(server_dto.server_name, server)
        service.reload()
        new_server_dto = crud.update_server(server_dto.id, server)
        if new_server_dto:
            return new_server_dto
    raise ValueError("Server não encontrado!")

@app.delete("/{id}")
def delete_server_endpoint(id: int):
    server_dto = crud.get_server_by_id(id)
    if server_dto:
        service.delete_server(server_dto.server_name)
        service.reload()
        crud.delete_server(server_dto.id)
        return JSONResponse(
            content={"message": f"{server_dto.server_name} deletado com sucesso!"}
        )
    raise ValueError("Server não encontrado!")

@app.exception_handler(ValueError)
async def exception_hangle(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )
