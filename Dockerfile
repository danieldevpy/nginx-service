FROM nginx:latest

# Instala o Certbot e dependências
RUN apt-get update && \
    apt-get install -y certbot python3-certbot-nginx && \
    apt-get clean
