from pydantic import BaseModel, ConfigDict, Field
from .merchant import Merchant
from .product import Product 
from typing import List
from datetime import date, datetime
from decimal import Decimal 

class ReceiptBase(BaseModel):
    merchant_id: int
    purchase_date: date
    barcode: str | None = Field(
        default=None, 
        max_length=20, 
        description="Barcode from receipt (optional)"
    )


class ReceiptCreate(ReceiptBase):
    pass

class ReceiptUpdate(BaseModel):
    merchant_id: int | None = None
    purchase_date: date | None = None
    barcode: str | None = Field(default=None, max_length=20)

class Receipt(ReceiptBase):
    id: int
    total_price: Decimal
    merchant: Merchant
    products: List[Product] = []
    created_at: datetime
    updated_at: datetime | None = None
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            date: lambda v: v.isoformat() if v else None,
            datetime: lambda v: v.isoformat() if v else None,
            Decimal: lambda v: float(v) if v else None
        }
    )

