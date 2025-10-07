# === STAGE 1: Build do frontend com Node ===
FROM node:20-alpine AS frontend-build

WORKDIR /app

# Copia package.json e package-lock.json
COPY nginxui/package*.json ./

# Instala dependências do frontend
RUN npm install

# Copia o restante do frontend
COPY nginxui/src src/
COPY nginxui/public ./
COPY nginxui/eslint.config.js nginxui/vite.config.ts \
    nginxui/tsconfig.node.json nginxui/tsconfig.json \
    nginxui/tsconfig.app.json nginxui/index.html \
    nginxui/.env ./

# Build do Vite (gera a pasta dist)
RUN npm run build

# Usa imagem oficial slim do Python
FROM python:3.11-slim

# Evita prompts interativos durante instalação
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Atualiza e instala apenas pacotes necessários em uma única camada
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nginx \
        certbot \
        python3-certbot-nginx \
        curl \
        procps \
        bash && \
    rm -rf /var/lib/apt/lists/*

# Copia apenas arquivos necessários para instalar dependências
COPY requirements.txt .

# Instala dependências do Python sem cache
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY backend nginxsrc/backend/
COPY core nginxsrc/core/
COPY --from=frontend-build /app/dist nginxsrc/ui/

# Expondo as portas necessárias
EXPOSE 80 443 8000

# Usa um entrypoint mais seguro e limpo
CMD ["bash", "-c", "service nginx start && uvicorn nginxsrc.backend.app:app --host 0.0.0.0 --reload"]
