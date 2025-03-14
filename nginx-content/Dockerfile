FROM nginx:latest

# Instala o Certbot e dependências
RUN apt-get update && \
    apt-get install -y certbot python3-certbot-nginx && \
    apt-get clean

# Copia os arquivos de configuração do Nginx
COPY ./nginx-content/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx-content/sites-available /etc/nginx/sites-available
COPY ./nginx-content/sites-enabled /etc/nginx/sites-enabled
COPY ./nginx-content/logs /var/log/nginx

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]