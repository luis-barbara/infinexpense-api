from pydantic import BaseModel, ConfigDict


class MerchantBase(BaseModel):
    name: str
    location: str | None = None


class MerchantCreate(MerchantBase):
    pass


class MerchantUpdate(BaseModel):
    name: str | None = None
    location: str | None = None


class Merchant(MerchantBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
