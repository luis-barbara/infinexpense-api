# Pydantic schema: serve para ir buscar informações aos models e transforma-las em json
# para depois permitir comunicar com frontend ou outras APIs

from pydantic import BaseModel, ConfigDict

class CategoryBase(BaseModel):
    name: str
    

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)   

