from pydantic import BaseModel, ConfigDict, Field

class CategoryBase(BaseModel):
    """Base schema for category"""
    name: str = Field(
        min_length=1, 
        max_length=100, 
        description="Name of the category (e.g., 'Fruit')"
    )
    
class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    """Schema for updating an existing category"""
    name: str | None = Field(
        default=None, 
        min_length=1, 
        max_length=100, 
        description="New name for the category (optional)"
    )
    color: str | None = Field(
        default=None,
        description="Hex color for the category (optional)"
    )

class Category(CategoryBase):
    """Complete category schema"""
    id: int
    color: str = Field(default="#808080", description="Hex color code")
    item_count: int = 0
    item_percentage: float = 0.0
    total_spent: float = 0.0
    model_config = ConfigDict(from_attributes=True)