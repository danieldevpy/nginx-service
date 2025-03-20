from fastapi import APIRouter, HTTPException
from models.schemas import (
    CreateRuleRequest,
    EditRuleRequest,
    InstallSSLRequest,
    UpdateFullRuleRequest,
)
from services.nginx_service import NginxService

router = APIRouter()

@router.get("/api/rules")
async def get_rules():
    return NginxService.get_rules()

@router.get("/api/rules/{server_name}")
async def get_rule(server_name: str):
    return NginxService.get_rule(server_name)

@router.post("/api/rules", status_code=201)
async def create_rule(request: CreateRuleRequest):
    return NginxService.create_rule(request.server_name, request.proxy_pass)

@router.post("/api/ssl")
async def install_ssl(request: InstallSSLRequest):
    return NginxService.install_ssl(request.domain, request.email)

@router.put("/api/rules/{server_name}")
async def update_rule(server_name: str, request: EditRuleRequest):
    return NginxService.update_rule(server_name, request.proxy_pass)

@router.put("/api/rules/{server_name}/full")
async def update_full_rule(server_name: str, request: UpdateFullRuleRequest):
    return NginxService.update_full_rule(server_name, request.config)

@router.delete("/api/rules/{server_name}")
async def delete_rule(server_name: str):
    return NginxService.delete_rule(server_name)

