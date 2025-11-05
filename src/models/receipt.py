from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship, CheckConstraint
from sqlalchemy.sql import func

from src.database import Base

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True) # Unique identifier for each receipt
    merchant_id = Column(Integer, ForeignKey("merchants.id", ondelete = "RESTRICT"), nullable=False) # Vendor name
    date = Column(Date, nullable=False) # Date of the receipt
    total_price = Column(Numeric(12,2), nullable=False) # Total amount on the receipt (000000.00)
    barcode = Column(Text, nullable=True) # Barcode number associated with the receipt
    notes = Column(Text, nullable=True) # Additional notes about the receipt

    merchant = relationship("Merchant", back_populates="receipts") # Relationship to the Merchant model
    items = relationship("ReceiptItem", back_populates="receipt", cascade="all, delete-orphan") # Relationship to ReceiptItem model

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) # Timestamp when the receipt was created
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) # Timestamp when the receipt was last updated

    __table_args__ = (CheckConstraint('total_price >= 0', name='constraint_check_negative_receipt'),)