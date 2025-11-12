from sqlalchemy import Column, Integer, String, Index, CheckConstraint
from sqlalchemy.orm import relationship

from src.database import Base

class MeasurementUnit(Base):
    """
    This class represents a Measurement Unit in the master list.
    (e.g., "Kilogram", "kg")
    
    This model corresponds to the MEASUREMENT_UNIT table in the database diagram
    and the 'MeasurementUnit' schemas in Pydantic.
    """

    __tablename__ = "measurement_unit"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(
        String(50), 
        nullable=False, 
        unique=True, 
        index=True, 
        info={'description':'Full name of the unit (e.g., "Kilogram")'}
    )
    
    abbreviation = Column(
        String(10), 
        nullable=False, 
        unique=True, 
        index=True, 
        info={'description':'Abbreviation of the unit (e.g., kg")'}
    )

    # The Relationship: "One unit (kg) can be in many product definitions (ProductList)"
    # This mirrors the relationship in 'ProductList'
    product_lists = relationship("ProductList", 
        back_populates="measurement_unit")

    # Indices to ensure name and abbreviation are unique
    __table_args__ = (
        Index('idx_measurement_unit_name_unique', 'name', unique=True),
        Index('idx_measurement_unit_abbreviation_unique', 'abbreviation', unique=True),
    )

    product_lists = relationship(
    "ProductList", 
    back_populates="measurement_unit",
    passive_deletes=False  # Will raise error if trying to delete unit with products
    )