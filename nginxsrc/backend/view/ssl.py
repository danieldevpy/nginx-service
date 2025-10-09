from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..instances import InstancesRepository
from ..controller.ssl import SSLController
from ..model.server import ServerDTO
from pydantic import BaseModel

controller = SSLController(
    server_repository=InstancesRepository().server_repository,
    ssl_service=InstancesRepository().ssl_service
)

router = APIRouter(
    prefix="/ssl",
    tags=["SSL"]
)

class InstallSSLRequest(BaseModel):
    id: int
    email: str

@router.post("/", response_model=ServerDTO)
def install_ssl_endpoint(request: InstallSSLRequest):
    try:
        return controller.install(request.id, request.email)
    except Exception as e:
        return JSONResponse({
            "message": str(e)
        }, status_code=400)