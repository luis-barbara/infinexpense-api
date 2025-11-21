# src/routers/measurement_units.py

from typing import List
from fastapi import APIRouter, Depends, status, Path, Query, HTTPException
from sqlalchemy.orm import Session
import logging

from src.database import get_db
from src.schemas.measurement_unit import (
    MeasurementUnitCreate,
    MeasurementUnitUpdate,
    MeasurementUnit as MeasurementUnitSchema
)
from src.services.crud_measurement_unit import MeasurementUnitService


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/measurement-units",
    tags=["Measurement Units"]
)

# Create
@router.post("/", response_model=MeasurementUnitSchema, status_code=status.HTTP_201_CREATED)
def create_measurement_unit(unit: MeasurementUnitCreate, db: Session = Depends(get_db)):
    try:
        return MeasurementUnitService.create_measurement_unit(db, unit)
    except ValueError as e:
        logger.warning(f"Validation error creating measurement unit: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error in create_measurement_unit endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating measurement unit"
        )

# Read All
@router.get("/", response_model=List[MeasurementUnitSchema])
def get_all_measurement_units(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    try:
        return MeasurementUnitService.get_measurement_units(db, skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Error in get_all_measurement_units endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching measurement units"
        )

# Read by ID
@router.get("/{unit_id}", response_model=MeasurementUnitSchema)
def get_measurement_unit_by_id(unit_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    try:
        unit = MeasurementUnitService.get_measurement_unit(db, unit_id)
        if not unit:
            logger.warning(f"Measurement unit not found: {unit_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Measurement Unit not found"
            )
        return unit
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching measurement unit {unit_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching measurement unit"
        )

# Update
@router.put("/{unit_id}", response_model=MeasurementUnitSchema)
def update_measurement_unit(unit_id: int, update_data: MeasurementUnitUpdate, db: Session = Depends(get_db)):
    try:
        unit = MeasurementUnitService.get_measurement_unit(db, unit_id)
        if not unit:
            logger.warning(f"Measurement unit not found for update: {unit_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Measurement Unit not found"
            )
        return MeasurementUnitService.update_measurement_unit(db, unit, update_data)
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Validation error updating measurement unit {unit_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating measurement unit {unit_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating measurement unit"
        )

# Delete
@router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_measurement_unit(unit_id: int, db: Session = Depends(get_db)):
    try:
        unit = MeasurementUnitService.get_measurement_unit(db, unit_id)
        if not unit:
            logger.warning(f"Measurement unit not found for deletion: {unit_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Measurement Unit not found"
            )
        MeasurementUnitService.delete_measurement_unit(db, unit)
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting measurement unit {unit_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting measurement unit"
        )
