from fastapi import HTTPException
from utils.nginx_utils import (
    create_nginx_config,
    validate_nginx_config,
    restart_nginx_container,
    install_ssl_certificate,
)
import os


class NginxService:

    @staticmethod
    def get_rules():
        try:
            path = r'/etc/nginx/sites-available/'
            files = []
            for raiz, _, files_in_dir in os.walk(path):
                for file in files_in_dir:
                    files.append(file.replace('.conf', ''))
            return files
        except FileNotFoundError:
            return f"Diretório não encontrado: {path}"
        except Exception as e:
            return f"Erro ao listar arquivos: {e}"

    @staticmethod
    def get_rule(server_name):
        config_path = f'/etc/nginx/sites-available/{server_name}.conf'
        if not os.path.exists(config_path):
            raise HTTPException(status_code=404, detail="Regra não encontrada")
        try:
            with open(config_path, 'r') as f:
                config_content = f.read()
            return {"server_name": server_name, "config": config_content}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def create_rule(server_name, proxy_pass):
        try:
            create_nginx_config(server_name, proxy_pass)
            restart_nginx_container()
            return {"message": "Regra criada com sucesso e Nginx reiniciado"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def update_rule(server_name, proxy_pass):
        config_path = f'/etc/nginx/sites-available/{server_name}.conf'
        if not os.path.exists(config_path):
            raise HTTPException(status_code=404, detail="Regra não encontrada")
        
        try:
            create_nginx_config(server_name, proxy_pass)
            restart_nginx_container()
            return {"message": "Regra atualizada com sucesso e Nginx reiniciado"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def update_full_rule(server_name, config_content):
        config_path = f'/etc/nginx/sites-available/{server_name}.conf'
        if not os.path.exists(config_path):
            raise HTTPException(status_code=404, detail="Regra não encontrada")
        
        try:
            validate_nginx_config(config_content)
            with open(config_path, 'w') as f:
                f.write(config_content)
            restart_nginx_container()
            return {"message": "Regra atualizada com sucesso e Nginx reiniciado"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def delete_rule(server_name):
        config_path = f'/etc/nginx/sites-available/{server_name}.conf'
        enabled_path = f'/etc/nginx/sites-enabled/{server_name}.conf'
        
        try:
            if os.path.exists(enabled_path):
                os.unlink(enabled_path)
            if os.path.exists(config_path):
                os.remove(config_path)
            restart_nginx_container()
            return {"message": "Regra removida com sucesso e Nginx reiniciado"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def install_ssl(domain, email):
        try:
            install_ssl_certificate(domain, email)
            return {"message": "Certificado SSL instalado com sucesso"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))