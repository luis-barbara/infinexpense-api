from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import CheckConstraint
import enum

from src.database import Base

class MeasurementType(enum.Enum):

    '''
    Enum for different types of measurements. 
    Besides 'weight' and 'volume', a generic 'unit' type is included for measurements
    that do not fit into the other categories.
    '''

    WEIGHT = "weight"
    VOLUME = "volume"
    UNIT = "unit"

class MeasurementUnit(enum.Enum):

    '''
    Enum for different measurement units.
    Includes common units for weight and volume, 
    as well as an 'other' category for less common units.
    '''

    KG = "kg"
    GRAMS = "grams"
    LITERS = "liters"
    MILLILITERS = "milliliters"
    OTHER = "other"


class Measurement(Base):

    '''
    This class represents a measurement in the system. 
    A measurement has a type (weight, volume, unit),
    a unit (kg, lt, g, ml, etc.), and a value. 
    The value must be non-negative.
    '''
    __tablename__ = "measurement"

    id = Column(Integer, primary_key=True, index=True) # Unique identifier for each measurement
    type = Column(String(20), nullable=False) # Type of measurement (weight, volume)
    unit = Column(String(10), nullable=False) # Unit of measurement (kg, lt, g, ml)
    value = Column(Numeric(12,4), nullable=False) # Value of the measurement (000000000000.0000)

    __table_args__ = (CheckConstraint('value >= 0', name='constraint_check_negative_value'),)