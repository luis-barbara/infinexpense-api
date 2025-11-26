from pydantic import BaseModel
from typing import Optional


class MerchantBase(BaseModel):
    """Base schema for merchant"""
    name: str
    location: str
    notes: Optional[str] = None


class MerchantCreate(BaseModel):
    """Schema for creating a new merchant."""
    name: str
    location: str
    notes: Optional[str] = None


class MerchantUpdate(BaseModel):
    """Schema for updating an existing merchant"""
    name: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    image_path: Optional[str] = None


class Merchant(MerchantBase):
    """Complete merchant schema"""
    id: int
    image_path: Optional[str] = None

    class ConfigDict:
        from_attributes = True
