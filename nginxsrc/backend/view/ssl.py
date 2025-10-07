from fastapi import APIRouter, HTTPException
from ..instances import InstancesRepository
from ..controller.ssl import SSLController

controller = SSLController(
    server_repository=InstancesRepository().server_repository,
    ssl_service=InstancesRepository().ssl_service
)

router = APIRouter(
    prefix="/ssl",
    tags=["SSL"]
)

@router.post("/")
def install_ssl_endpoint(id: int, email: str):
    return controller.install(id, email)