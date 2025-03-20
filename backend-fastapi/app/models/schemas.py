from pydantic import BaseModel

class CreateRuleRequest(BaseModel):
    server_name: str
    proxy_pass: str

class EditRuleRequest(BaseModel):
    proxy_pass: str

class InstallSSLRequest(BaseModel):
    domain: str
    email: str

class UpdateFullRuleRequest(BaseModel):
    config: str