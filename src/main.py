from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from src.routers import receipts  # make sure this import works

# Base directory: project root (/app when inside Docker)
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="Infinexpense API",
    description="See Where Your Money Really Goes.",
    version="0.1.0",
)

# --- API routers ---
# Use ONE prefix for /receipts, not two:
app.include_router(receipts.router)
# If your APIRouter already has prefix="/receipts", then instead do:
# app.include_router(receipts.router)

# --- Static files ---
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# --- HTML homepage ---
@app.get("/", include_in_schema=False)
def read_root():
    index_path = STATIC_DIR / "index.html"
    return FileResponse(index_path)

