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

    product_lists = relationship("ProductList", back_populates="measurement_unit", passive_deletes=False)

    __table_args__ = (
        Index('idx_measurement_unit_name_unique', 'name', unique=True),
        Index('idx_measurement_unit_abbreviation_unique', 'abbreviation', unique=True),
    )