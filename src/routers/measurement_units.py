# src/routers/measurement_units.py

from typing import List
from fastapi import APIRouter, Depends, status, Path, Query, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.measurement_unit import (
    MeasurementUnitCreate,
    MeasurementUnitUpdate,
    MeasurementUnit as MeasurementUnitSchema
)
from src.services.crud_measurement_unit import MeasurementUnitService

router = APIRouter(
    prefix="/measurement-units",
    tags=["Measurement Units"]
)

# Create
@router.post("/", response_model=MeasurementUnitSchema, status_code=status.HTTP_201_CREATED)
def create_measurement_unit(unit: MeasurementUnitCreate, db: Session = Depends(get_db)):
    return MeasurementUnitService.create_measurement_unit(db, unit)

# Read All
@router.get("/", response_model=List[MeasurementUnitSchema])
def get_all_measurement_units(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    return MeasurementUnitService.get_measurement_units(db, skip=skip, limit=limit)

# Read by ID
@router.get("/{unit_id}", response_model=MeasurementUnitSchema)
def get_measurement_unit_by_id(unit_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    unit = MeasurementUnitService.get_measurement_unit(db, unit_id)
    if not unit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Measurement Unit not found")
    return unit

# Update
@router.put("/{unit_id}", response_model=MeasurementUnitSchema)
def update_measurement_unit(unit_id: int, update_data: MeasurementUnitUpdate, db: Session = Depends(get_db)):
    unit = MeasurementUnitService.get_measurement_unit(db, unit_id)
    if not unit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Measurement Unit not found")
    return MeasurementUnitService.update_measurement_unit(db, unit, update_data)

# Delete
@router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_measurement_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = MeasurementUnitService.get_measurement_unit(db, unit_id)
    if not unit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Measurement Unit not found")
    MeasurementUnitService.delete_measurement_unit(db, unit)
    return None
