from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import CheckConstraint
import enum

from src.database import Base

class MeasurementType(enum.Enum):
    WEIGHT = "weight"
    VOLUME = "volume"
    UNIT = "unit"

class MeasurementUnit(enum.Enum):
    KG = "kg"
    GRAMS = "grams"
    LITERS = "liters"
    MILLILITERS = "milliliters"
    OTHER = "other"


class Measurement(Base):
    __tablename__ = "measurement"

    id = Column(Integer, primary_key=True, index=True) # Unique identifier for each measurement
    type = Column(String(20), nullable=False) # Type of measurement (weight, volume)
    unit = Column(String(10), nullable=False) # Unit of measurement (kg, lt, g, ml)
    value = Column(Numeric(12,4), nullable=False) # Value of the measurement (000000000000.0000)



    __table_args__ = (CheckConstraint('value >= 0', name='constraint_check_negative_value'),)