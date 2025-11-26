from pydantic import BaseModel, ConfigDict, Field

class MeasurementUnitBase(BaseModel):
    """Base schema for measurement unit"""
    name: str = Field(max_length=50, description="Full name of the unit (e.g., 'Kilogram')")
    abbreviation: str = Field(max_length=10, description="Unit abbreviation (e.g., 'kg')")

class MeasurementUnitCreate(MeasurementUnitBase):
    """Schema for creating a new measurement unit."""
    pass

class MeasurementUnitUpdate(BaseModel):
    """
    Schema used for updating a Measurement Unit.
    """
    name: str | None = Field(default=None, max_length=50)
    abbreviation: str | None = Field(default=None, max_length=10)

class MeasurementUnit(MeasurementUnitBase):
    """Complete measurement unit schema"""
    id: int
    model_config = ConfigDict(from_attributes=True)