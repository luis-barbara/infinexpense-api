# src/main.py 

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import logging
import time

from src.routers import (
    receipts, 
    products, 
    categories, 
    merchants, 
    measurement_units,
    reports,  
    uploads   
)

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = BASE_DIR / "static" 

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Logs Directory
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Logging Configuration
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        RotatingFileHandler(
            LOG_DIR / "app.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,  # Keep 5 backup files
            encoding='utf-8'
        )
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Infinexpense API starting up...")
    logger.info(f"Static directory: {STATIC_DIR}")
    logger.info(f"Upload directory: {UPLOAD_DIR}")
    yield
    # Shutdown
    logger.info("Infinexpense API shutting down...")


app = FastAPI(
    title="Infinexpense API",
    description="See Where Your Money Really Goes.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logar requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log da request recebida
    logger.info(f"→ {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    # Log da resposta com tempo de processamento
    process_time = time.time() - start_time
    logger.info(f"← {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.3f}s")
    
    return response

# API Routers
# Routers de CRUD
app.include_router(receipts.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(merchants.router)
app.include_router(measurement_units.router)
app.include_router(reports.router)
app.include_router(uploads.router)

logger.info("All routers registered successfully")


# Montagem de Ficheiros Estáticos (Static Files)
# Para o Frontend (HTML/CSS/JS)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Para as Fotos dos Produtos
app.mount("/css", StaticFiles(directory=str(STATIC_DIR / "css")), name="css")
app.mount("/js", StaticFiles(directory=str(STATIC_DIR / "js")), name="js")
app.mount("/images", StaticFiles(directory=str(STATIC_DIR / "images")), name="images")
app.mount("/templates", StaticFiles(directory=str(STATIC_DIR / "templates")), name="templates")
app.mount("/api", StaticFiles(directory=str(STATIC_DIR / "api")), name="api")
app.mount("/category", StaticFiles(directory=str(STATIC_DIR / "category")), name="category")
app.mount("/merchant", StaticFiles(directory=str(STATIC_DIR / "merchant")), name="merchant")
app.mount("/product", StaticFiles(directory=str(STATIC_DIR / "product")), name="product")
app.mount("/receipt", StaticFiles(directory=str(STATIC_DIR / "receipt")), name="receipt")
app.mount("/docs", StaticFiles(directory=str(STATIC_DIR / "docs")), name="docs")
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")


@app.get("/", include_in_schema=False)
def read_root():
    """Serve the homepage from static directory."""
    index_path = STATIC_DIR / "index.html"
    if not index_path.is_file():
        return {"error": "index.html not found in static directory"}, 404
    return FileResponse(index_path)

@app.get("/index.html", include_in_schema=False)
def read_index():
    """Serve index.html directly."""
    index_path = STATIC_DIR / "index.html"
    if not index_path.is_file():
        logger.warning("index.html not found in static directory")
        return {"error": "index.html not found in static directory"}, 404
    return FileResponse(index_path)



