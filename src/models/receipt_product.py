from sqlalchemy import Column, Integer, String, ForeignKey, Index, Numeric, CheckConstraint
from sqlalchemy.orm import relationship
from src.models.product import ProductList
from src.database import Base

class Product(Base):
    """
    This class represents an "item" on a receipt.
    (e.D., The specific instance of "Banana" that was bought: 0.5kg at 1.25€)
    
    This model corresponds to the PRODUCT table in the database diagram
    and the 'Product' schemas in Pydantic.
    """

    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    
    price = Column(
        Numeric(12, 4), 
        nullable=False, 
        info={'description':'Price of this specific item"'}
    )
    quantity = Column(
        Numeric(12, 4), 
        nullable=False, 
        info={'description':'Quantity of this specific item (e.g., 0.5)"'}
    )
    
    description = Column(
        String(100), 
        nullable=True, 
        info={'description':'Optional description (e.g., "on sale")'}
    )

    receipt_id = Column(
        Integer, 
        ForeignKey("receipts.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    product_list_id = Column(
        Integer, 
        ForeignKey("product_list.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    receipt = relationship("Receipt", back_populates="products")
    product_list = relationship("ProductList", back_populates="products")

    __table_args__ = (
        CheckConstraint('price >= 0', name='constraint_check_product_price_negative'),
        CheckConstraint('quantity > 0', name='constraint_check_product_quantity_zero'),
    )