# === STAGE 1: Build do frontend com Node ===
FROM node:20-alpine AS frontend-build

WORKDIR /app/nginxui

# Copia apenas package.json e package-lock.json
COPY nginxui/package*.json ./

# Instala dependências do frontend
RUN npm install

# Copia o restante do frontend
COPY nginxui/ .

# Build do frontend com Vite (gera a pasta dist)
RUN npm run build

# === STAGE 2: Backend com Python + Nginx ===
FROM python:3.11-slim

# Evita prompts interativos
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Instala apenas pacotes necessários
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nginx \
        certbot \
        python3-certbot-nginx \
        curl \
        procps \
        bash && \
    rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia backend e core
COPY backend ./nginxsrc/backend/
COPY core ./nginxsrc/core/

# Copia frontend build (apenas conteúdo de dist) para templates
COPY --from=frontend-build /app/nginxui/dist/ /app/dist/

# Copia entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expõe portas
EXPOSE 80 443 8000

# Entrypoint
ENTRYPOINT ["/entrypoint.sh"]
