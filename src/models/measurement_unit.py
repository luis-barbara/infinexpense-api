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
        description="Full name of the unit (e.g., 'Kilogram')"
    )
    
    abbreviation = Column(
        String(10), 
        nullable=False, 
        unique=True, 
        index=True, 
        description="Abbreviation of the unit (e.g., 'kg')"
    )

    # The Relationship: "One unit (kg) can be in many product definitions (ProductList)"
    # This mirrors the relationship in 'ProductList'
    product_lists = relationship("ProductList", back_populates="measurement_unit")

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

## CORRECTION

from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship, validates

from src.database import Base

class MeasurementUnit(Base):
    """
    Represents a measurement unit in the master list.
    
    Examples: ("Kilogram", "kg"), ("Liter", "L"), ("Unit", "unit")
    
    This model corresponds to the MEASUREMENT_UNIT table in the database diagram
    and the 'MeasurementUnit' schemas in Pydantic.
    """

    __tablename__ = "measurement_unit"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(
        String(50), 
        nullable=False, 
        unique=True, 
        index=True
    )
    
    abbreviation = Column(
        String(10), 
        nullable=False, 
        unique=True, 
        index=True
    )

    # Relationships
    product_lists = relationship(
        "ProductList", 
        back_populates="measurement_unit",
        cascade="all, delete-orphan"  # Optional: depends on your business logic
    )

    # Constraints
    __table_args__ = (
        CheckConstraint("LENGTH(TRIM(name)) > 0", name="check_name_not_empty"),
        CheckConstraint("LENGTH(TRIM(abbreviation)) > 0", name="check_abbreviation_not_empty"),
    )

    # Validation
    @validates('name', 'abbreviation')
    def validate_not_empty(self, key, value):
        """Ensure name and abbreviation are not empty or whitespace-only."""
        if not value or not value.strip():
            raise ValueError(f"{key} cannot be empty or whitespace")
        return value.strip()

    def __repr__(self):
        return f"<MeasurementUnit(id={self.id}, name='{self.name}', abbreviation='{self.abbreviation}')>"