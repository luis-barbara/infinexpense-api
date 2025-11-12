# Pydantic schema: serve para ir buscar informações aos models e transforma-las em json
# para depois permitir comunicar com frontend ou outras APIs

from pydantic import BaseModel, ConfigDict, Field

# Base schema for Category
class CategoryBase(BaseModel):
    name: str = Field(
        min_length=1, 
        max_length=100, 
        description="Name of the category (e.g., 'Fruit')"
    )
    
# Schema used for creating a new Category
class CategoryCreate(CategoryBase):
    pass

# Schema used for updating a Category
class CategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None, 
        min_length=1, 
        max_length=100, 
        description="New name for the category (optional)"
    )

# Schema representing a Category with its ID (Read Schema)
class Category(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)   