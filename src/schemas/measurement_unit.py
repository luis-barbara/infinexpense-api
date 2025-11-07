from pydantic import BaseModel, ConfigDict, Field

# Baese schema for Measurement Unit
class MeasurementUnitBase(BaseModel):
    name: str = Field(max_length=50, description="Full name of the unit (e.g., 'Kilogram')")
    abbreviation: str = Field(max_length=10, description="Unit abbreviation (e.g., 'kg')")

# Schema used for creating a new Measurement Unit
class MeasurementUnitCreate(MeasurementUnitBase):
    pass

# Schema used for updating a Measurement Unit
class MeasurementUnitUpdate(BaseModel):
    """
    Schema used for updating a Measurement Unit.
    All fields are optional.
    """
    name: str | None = Field(default=None, max_length=50)
    abbreviation: str | None = Field(default=None, max_length=10)

# Schema representing a Measurement Unit with its ID (Read Schema)
class MeasurementUnit(MeasurementUnitBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
