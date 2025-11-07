from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, String, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database import Base

class Receipt(Base):
    
    '''
    This class represents a receipt in the system.
    A receipt is associated with a merchant, has a date, total price,
    an optional barcode, and optional notes. It also maintains relationships
    with the Merchant and ReceiptItem models.
    The total price must be non-negative.
    '''

    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True) # Unique identifier for each receipt
    merchant_id = Column(Integer, ForeignKey("merchants.id", ondelete = "RESTRICT"), nullable=False) # Vendor name
    date = Column(Date, nullable=False, Index=True) # Date of the receipt
    
    barcode = Column(String(20), nullable=True) # Barcode number associated with the receipt
    

    merchant = relationship("Merchant", back_populates="receipts") # Relationship to the Merchant model
    products = relationship("Product", back_populates="receipt", cascade="all, delete-orphan") # Relationship to Product model

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) # Timestamp when the receipt was created
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) # Timestamp when the receipt was last updated

    