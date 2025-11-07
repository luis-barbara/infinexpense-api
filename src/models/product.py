## LUIS
 
from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship

from src.database import Base

class ProductList(Base):
    """
    This class represents an item in the "Master List" of Products.
    (e.g., The definition of "Banana", which is "Fruit" and "kg")
    
    This model corresponds to the PRODUCT_LIST table in the database diagram
    and the 'ProductList' schemas in Pydantic.
    """

    __tablename__ = "product_list"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(
        String(255), 
        nullable=False, 
        unique=True, 
        index=True, 
        description="Name of the product (e.g., 'Madeira Banana')"
    )
    

    barcode = Column(
        String(50), 
        nullable=True, 
        unique=True, 
        index=True, 
        description="Barcode of the product (optional, unique)"
    )

    
    category_id = Column(
        Integer, 
        ForeignKey("category.id", ondelete="RESTRICT"), 
        nullable=False,
        index=True
    )
    
    measurement_unit_id = Column(
        Integer, 
        ForeignKey("measurement_unit.id", ondelete="RESTRICT"), 
        nullable=False,
        index=True
    )

    category = relationship("Category", back_populates="product_lists")
    measurement_unit = relationship("MeasurementUnit", back_populates="product_lists")
    products = relationship("Product", back_populates="product_list")

    __table_args__ = (
        Index('idx_product_list_name_unique', 'name', unique=True),
        Index('idx_product_list_barcode_unique', 'barcode', unique=True, postgresql_where=barcode.isnot(None)),
    )