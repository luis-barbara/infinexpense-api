## LUIS

from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship

from src.database import Base


class Category(Base):
    """
    This class represents a Category in the master list.
    (e.g., "Dairy", "Fruit", "Meat")
    
    This model corresponds to the CATEGORY table in the database diagram
    and the 'Category' schemas in Pydantic.
    """

    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(
        String(100), 
        nullable=False, 
        unique=True, 
        index=True, 
        description="Name of the category (e.g., 'Fruit')"
    )

    # The Relationship: "One category can be in many product definitions (ProductList)"
    # This mirrors the relationship in 'product.py'
    product_lists = relationship("ProductList", back_populates="category")


    __table_args__ = (
        Index('idx_category_name_unique', 'name', unique=True),
    )