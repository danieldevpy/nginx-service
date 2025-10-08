from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from .view import server, settings, ssl
from pathlib import Path

BASE_DIR = Path("/app/dist")

app = FastAPI(title="API de Servidores")

app.mount("/assets", StaticFiles(directory=BASE_DIR / "assets"), name="assets")

@app.get("/")
async def serve_index():
    return FileResponse(BASE_DIR / "index.html")

@app.get("/{file_name}")
async def serve_file(file_name: str):
    file_path = BASE_DIR / file_name
    if file_path.exists():
        return FileResponse(file_path)
    return {"error": "File not found"}

@app.exception_handler(ValueError)
async def exception_hangle(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )

app.include_router(settings.router)
app.include_router(server.router)
app.include_router(ssl.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # aceita de qualquer lugar
    allow_credentials=True,
    allow_methods=["*"],  # aceita GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # aceita qualquer header
)