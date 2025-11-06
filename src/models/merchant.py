from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship, CheckConstraint

from src.database import Base


class Merchant(Base):

    """
    This class represents a merchant in the system. A merchant has a name (unique), 
    can have multiple receipts associated (relationship),
    and may have additional notes about them. Note that the merchant name cannot be empty.
    """

    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True) # Unique identifier for each merchant
    name = Column(String(100), nullable=False, unique=True, Index=True) # Name of the merchant
    receipts = relationship("Receipt", back_populates="merchant", cascade="all, delete-orphan") # Relationship to Receipt model
    notes = Column(Text, nullable=True) # Additional notes about the merchant


    CheckConstraint('name != ""', name='constraint_check_empty_merchant_name')
