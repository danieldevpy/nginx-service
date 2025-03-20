from fastapi import FastAPI
from controllers.nginx_controller import router as nginx_router

app = FastAPI()
app.include_router(nginx_router)

@app.get("/")
async def root():
    return {"message": "Nginx Manager API"}