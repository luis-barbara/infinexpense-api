from pydantic import BaseModel, ConfigDict, Field
from .category import Category
from .measurement_unit import MeasurementUnit
from typing import List
from decimal import Decimal

# schemas para Lista de Produtos (PRODUCT_LIST)
class ProductListBase(BaseModel):
    name: str = Field(
        min_length=1, 
        max_length=255, 
        description="Name of the product (e.g., 'Banana')"
    )
    barcode: str | None = Field(
        default=None, 
        max_length=50, 
        description="Barcode of the product (optional, unique)"
    )
    measurement_unit_id: int 
    category_id: int 

class ProductListCreate(ProductListBase):
    pass

class ProductListUpdate(BaseModel):
    name: str | None = Field(
        default=None, 
        min_length=1, 
        max_length=255,
        description="New name for the product (optional)"
    )
    barcode: str | None = Field(
        default=None, 
        max_length=50,
        description="New barcode for the product (optional)"
    )
    measurement_unit_id: int | None = None
    category_id: int | None = None

class ProductList(ProductListBase):
    id: int
    category: Category 
    measurement_unit: MeasurementUnit 
    model_config = ConfigDict(from_attributes=True)


# schemas para item do Recibo (PRODUCT)
class ProductBase(BaseModel):
    price: Decimal = Field(
        max_digits=12, 
        decimal_places=4, 
        description="Price of the item (e.g., 1.25)"
    )
    quantity: Decimal = Field(
        max_digits=12, 
        decimal_places=4, 
        description="Quantity of the item (e.g., 0.5)"
    )
    description: str | None = Field(
        default=None, 
        max_length=100, 
        description="Optional description (e.g., 'on sale')"
    )
    product_list_id: int

class ProductCreate(ProductBase):   
    pass

class ProductUpdate(BaseModel):
    price: Decimal | None = Field(default=None, max_digits=12, decimal_places=4)
    quantity: Decimal | None = Field(default=None, max_digits=12, decimal_places=4)
    description: str | None = Field(default=None, max_length=100)
    product_list_id: int | None = None

class Product(ProductBase):
    id: int
    product_list: ProductList
    model_config = ConfigDict(from_attributes=True)