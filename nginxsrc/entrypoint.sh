#!/bin/bash
set -e

# Inicia Nginx em background
echo "Iniciando Nginx..."
service nginx start

# Inicia Uvicorn
echo "Iniciando Uvicorn..."
exec uvicorn nginxsrc.backend.app:app --host 0.0.0.0 --port 8000
