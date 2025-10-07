from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .view import server, settings, ssl

app = FastAPI(title="API de Servidores")

app.include_router(server.router)
app.include_router(settings.router)
app.include_router(ssl.router)

@app.exception_handler(ValueError)
async def exception_hangle(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )

# permite qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # aceita de qualquer lugar
    allow_credentials=True,
    allow_methods=["*"],  # aceita GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # aceita qualquer header
)
