from pydantic import BaseModel, ConfigDict, Field, field_serializer
from .merchant import Merchant
from .product import Product
from typing import List
from datetime import date, datetime
from decimal import Decimal


class ReceiptBase(BaseModel):
    merchant_id: int
    purchase_date: date
    barcode: str | None = Field(default=None, max_length=20)
    receipt_photo: str | None = Field(default=None, max_length=500)


class ReceiptCreate(ReceiptBase):
    pass


class ReceiptUpdate(BaseModel):
    merchant_id: int | None = None
    purchase_date: date | None = None
    barcode: str | None = Field(default=None, max_length=20)
    receipt_photo: str | None = Field(default=None, max_length=500)


class Receipt(ReceiptBase):
    id: int
    total_price: Decimal
    merchant: Merchant
    products: List[Product] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

    # Serializers for Pydantic 2.x
    @field_serializer("purchase_date", "created_at", "updated_at")
    def serialize_dates(self, value, _info):
        return value.isoformat() if value else None

    @field_serializer("total_price")
    def serialize_decimal(self, value: Decimal, _info):
        return float(value) if value is not None else None
