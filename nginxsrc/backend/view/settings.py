from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import Dict
from ..instances import InstancesRepository
from ..controller.settings import SettingsController

controller = SettingsController(
    settings_service=InstancesRepository().settings_service
)

router = APIRouter(
    prefix="/settings",
    tags=["Settings"]
)

@router.get(
    path="/status",
    summary="Retorna status do sistema"
)
def get_status() -> Dict[str, str]:
    """
    Retorna informações gerais ou status atual do sistema.
    """
    return {"message": controller.status()}

@router.get(
    path="/reload",
    summary="Reiniciar o serviço"
)
def reload():
    """
    Reinicia o serviço do NGINX
    """
    controller.reload()

@router.get(
    path="/clean_servers",
    summary="Remove todos os arquivos de config de servidores."
)
def clean_servers():
    return controller.clean_servers()