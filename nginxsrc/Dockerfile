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
COPY nginxui/dist nginxsrc/ui/

# Expondo as portas necessárias
EXPOSE 80 443 8000

# Usa um entrypoint mais seguro e limpo
CMD ["bash", "-c", "service nginx start && uvicorn nginxsrc.backend.app:app --host 0.0.0.0 --reload"]
