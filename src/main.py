from fastapi import FastAPI
from app.routers import receipts, products, merchants, categories, reports

app = FastAPI(
    title="Infinexpense API",
    description="See Where Your Money Really Goes.",
    version="0.1.0"
)

app.include_router(receipts.router, prefix="/receipts", tags=["Receipts"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(merchants.router, prefix="/merchants", tags=["Merchants"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])



@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint returning a welcome message.
    """
    return {"Hello": "Welcome to Infinexpense API"}


