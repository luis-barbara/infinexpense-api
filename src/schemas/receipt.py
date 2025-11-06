from pydantic import BaseModel, ConfigDict
from .merchant import Merchant
from .product import Product
from typing import List
from datetime import datetime

class Receipt(BaseModel):
    merchant_id: int
    barcode: str
    purchase_date: datetime

class ReceiptCreate(ReceiptBase):
    pass

class ReceiptUpdate(BaseModel):
    merchant_id: int | None = None
    barcode: str | None = None
    purchase_date: datetime | None = None

class Receipt(ReceiptBase):
    id: int
    total_price: float
    merchant: Merchant
    products: List[Product] = []
    model_config = ConfigDict(from_attributes=True)
