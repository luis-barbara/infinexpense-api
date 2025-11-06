from pydantic import BaseModel, ConfigDict
from .category import Category
from .measurement_unit import MeasurementUnit

# schemas para Lista de Produtos (PRODUCT_LIST)
class ProductListBase(BaseModel):
    name: str
    barcode: str | None = None
    measurement_unit_id: int 
    category_id: int 

class ProductListCreate(ProductListBase):
    pass

class ProductListUpdate(BaseModel):
    name: str | None = None
    barcode: str | None = None
    measurement_unit_id: int | None = None
    category_id: int | None = None

class ProductList(ProductListBase):
    id: int
    category: Category 
    measurement_unit: MeasurementUnit 
    model_config = ConfigDict(from_attributes=True)


# schemas para item do Recibo (PRODUCT)
class ProductBase(BaseModel):
    price: float
    quantity: float
    description: str | None = None
    product_list_id: int

class ProductCreate(ProductBase):   
    pass

class ProductUpdate(BaseModel):
    price: float | None = None
    quantity: float | None = None
    description: str | None = None
    product_list_id: int | None = None

class Product(ProductBase):
    id: int
    product_list: ProductList
    model_config = ConfigDict(from_attributes=True)
