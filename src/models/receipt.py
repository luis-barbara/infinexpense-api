# src/models/receipt.py
from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, String, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from decimal import Decimal
from src.models.merchant import Merchant
from src.models.receipt_product import Product
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
    
    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id", ondelete="RESTRICT"), nullable=False)
    purchase_date = Column(Date, nullable=False, index=True)
    barcode = Column(String(20), nullable=True)
    total_price = Column(Numeric(10, 2), default=Decimal('0.00'), nullable=False) 
    receipt_photo = Column(String(500), nullable=True)
    
    merchant = relationship("Merchant", back_populates="receipts")
    products = relationship("Product", back_populates="receipt", cascade="all, delete-orphan")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())