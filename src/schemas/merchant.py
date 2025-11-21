from pydantic import BaseModel
from typing import Optional


class MerchantBase(BaseModel):
    name: str
    location: str
    notes: Optional[str] = None


class MerchantCreate(BaseModel):
    name: str
    location: str
    notes: Optional[str] = None


class MerchantUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    image_path: Optional[str] = None


class Merchant(MerchantBase):
    id: int
    image_path: Optional[str] = None

    class ConfigDict:
        from_attributes = True
