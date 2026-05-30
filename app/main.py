from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
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

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html lang='es'>
    <head>
        <meta charset='UTF-8'>
        <title>Generador de Recetas</title>
        <link rel='icon' href='/static/favicon.ico' type='image/x-icon'>
        <style>body{font-family:Arial;max-width:600px;margin:60px auto;text-align:center;color:#333}</style>
    </head>
    <body>
        <h1>Generador de Recetas con IA</h1>
        <p>API funcionando correctamente.</p>
        <a href='/docs'>Ver documentacion Swagger</a>
    </body>
    </html>
    """
