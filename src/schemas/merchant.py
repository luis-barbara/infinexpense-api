from pydantic import BaseModel, ConfigDict, Field


class MerchantBase(BaseModel):
    name: str = Field(
        min_length=1, 
        max_length=100, 
        description="Name of the merchant (required, 1-100 characters)"
    )
    location: str | None = Field(
        default=None, 
        description="Optional location of the merchant (e.g., 'Olhao', 'Faro')"
    )


class MerchantCreate(MerchantBase):
    pass


class MerchantUpdate(BaseModel):
    name: str | None = Field(
        default=None, 
        min_length=1, 
        max_length=100, 
        description="New name for the merchant (optional)"
    )
    location: str | None = Field(
        default=None, 
        description="New location for the merchant (optional)"
    )


class Merchant(MerchantBase):
    id: int
    model_config = ConfigDict(from_attributes=True)