# Documentação das Rotas da API

## 1. Obter todas as regras de proxy
**Endpoint:** `GET /api/rules`

**Descrição:** Retorna uma lista com todas as regras de proxy configuradas no Nginx.

**Resposta de Exemplo:**
```json
[
  {
    "server_name": "example.com",
    "proxy_pass": "http://localhost:3000"
  },
  {
    "server_name": "api.example.com",
    "proxy_pass": "http://localhost:8000"
  }
]
```

## 2. Obter uma regra específica pelo nome do servidor
**Endpoint:** `GET /api/rules/{server_name}`

**Descrição:** Retorna a configuração de uma regra de proxy específica.

**Parâmetros:**
- `server_name` (string) - Nome do servidor da regra desejada.

**Resposta de Exemplo:**
```json
{
  "server_name": "example.com",
  "proxy_pass": "http://localhost:3000"
}
```

## 3. Criar uma nova regra de proxy
**Endpoint:** `POST /api/rules`

**Descrição:** Cria uma nova regra de proxy no Nginx.

**Requisição:**
```json
{
  "server_name": "example.com",
  "proxy_pass": "http://localhost:3000"
}
```

**Resposta:**
- `201 Created` caso a regra seja criada com sucesso.
- Corpo da resposta retorna a nova configuração.

**Resposta de Exemplo:**
```json
{
  "server_name": "example.com",
  "proxy_pass": "http://localhost:3000"
}
```

## 4. Instalar SSL em um domínio
**Endpoint:** `POST /api/ssl`

**Descrição:** Instala um certificado SSL para um domínio específico.

**Requisição:**
```json
{
  "domain": "example.com",
  "email": "admin@example.com"
}
```

**Resposta de Exemplo:**
```json
{
  "message": "SSL instalado com sucesso para example.com"
}
```

## 5. Atualizar uma regra de proxy existente
**Endpoint:** `PUT /api/rules/{server_name}`

**Descrição:** Atualiza a regra de proxy de um servidor específico.

**Parâmetros:**
- `server_name` (string) - Nome do servidor a ser atualizado.

**Requisição:**
```json
{
  "proxy_pass": "http://localhost:5000"
}
```

**Resposta de Exemplo:**
```json
{
  "server_name": "example.com",
  "proxy_pass": "http://localhost:5000"
}
```

## 6. Atualizar a configuração completa de uma regra
**Endpoint:** `PUT /api/rules/{server_name}/full`

**Descrição:** Atualiza toda a configuração de um servidor no Nginx.

**Parâmetros:**
- `server_name` (string) - Nome do servidor.

**Requisição:**
```json
{
  "config": "server { listen 80; server_name example.com; location / { proxy_pass http://localhost:5000; } }"
}
```

**Resposta de Exemplo:**
```json
{
  "message": "Configuração do servidor example.com atualizada com sucesso"
}
```

## 7. Remover uma regra de proxy
**Endpoint:** `DELETE /api/rules/{server_name}`

**Descrição:** Remove uma regra de proxy do Nginx.

**Parâmetros:**
- `server_name` (string) - Nome do servidor a ser removido.

**Resposta de Exemplo:**
```json
{
  "message": "Regra de proxy removida com sucesso para example.com"
}
```

