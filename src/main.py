# src/main.py 

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

# Imports dos Routers 

from src.routers import (
    receipts, 
    products, 
    categories, 
    merchants, 
    measurement_units,
    reports,  
    uploads   
)

# Definição dos Caminhos (Paths)

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = BASE_DIR / "static" 

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


app = FastAPI(
    title="Infinexpense API",
    description="See Where Your Money Really Goes.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
# Routers de CRUD
app.include_router(receipts.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(merchants.router)
app.include_router(measurement_units.router)

# Router de Reports
app.include_router(reports.router)

# Router de Uploads
app.include_router(uploads.router)


# Montagem de Ficheiros Estáticos (Static Files)
# Para o Frontend (HTML/CSS/JS)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Para as Fotos dos Produtos
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")


# Servidor da Homepage (HTML)
@app.get("/", include_in_schema=False)
def read_root():
    """
    Serve a página principal (index.html) do teu frontend
    que está na pasta /static.
    """
    index_path = STATIC_DIR / "index.html"
    if not index_path.is_file():
        return {"error": "index.html not found in static directory"}, 404
    return FileResponse(index_path)



