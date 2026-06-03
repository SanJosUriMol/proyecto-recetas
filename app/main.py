from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from app.database import Base, engine
from app.routers import auth, ingredientes, recetas

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Generador de Recetas con IA",
    description="API REST para gestionar ingredientes y generar recetas usando LLM",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router)
app.include_router(ingredientes.router)
app.include_router(recetas.router)

@app.get("/", response_class=FileResponse)
def root():
    return FileResponse("static/index.html")