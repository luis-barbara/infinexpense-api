from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from src.models import measurement_unit as measurement_unit_model
from src.schemas import measurement_unit as measurement_unit_schema


class MeasurementUnitService:
    @staticmethod
    def get_measurement_unit(db: Session, measurement_unit_id: int) -> Optional[measurement_unit_model.MeasurementUnit]:
        """Get a measurement unit by ID."""
        return db.query(measurement_unit_model.MeasurementUnit).filter(
            measurement_unit_model.MeasurementUnit.id == measurement_unit_id).first()

    @staticmethod
    def get_measurement_units(db: Session, skip: int = 0, limit: int = 100) -> List[measurement_unit_model.MeasurementUnit]:
        """Get all measurement units with pagination."""
        return (
            db.query(measurement_unit_model.MeasurementUnit)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create_measurement_unit(db: Session, measurement_unit_data: measurement_unit_schema.MeasurementUnitCreate) -> measurement_unit_model.MeasurementUnit:
        """Create a new measurement unit."""
        existing = db.query(measurement_unit_model.MeasurementUnit).filter_by(name=measurement_unit_data.name).first()
        if existing:
            raise ValueError(f"Measurement Unit '{measurement_unit_data.name}' already exists.")

        db_measurement_unit = measurement_unit_model.MeasurementUnit(**measurement_unit_data.model_dump())
        db.add(db_measurement_unit)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

        db.refresh(db_measurement_unit)
        return db_measurement_unit



    @staticmethod
    def update_measurement_unit(db: Session, db_measurement_unit: measurement_unit_model.MeasurementUnit, update_data: measurement_unit_schema.MeasurementUnitUpdate) -> measurement_unit_model.MeasurementUnit:
        """Update a measurement unit."""
        update_dict = update_data.model_dump(exclude_unset=True)
        if 'name' in update_dict:
            existing = db.query(measurement_unit_model.MeasurementUnit).filter_by(name=update_dict['name']).first()
            if existing and existing.id != db_measurement_unit.id:
                raise ValueError(f"Measurement Unit '{update_dict['name']}' already exists.")

        for key, value in update_dict.items():
            setattr(db_measurement_unit, key, value)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

        db.refresh(db_measurement_unit)
        return db_measurement_unit



    @staticmethod
    def delete_measurement_unit(db: Session, db_measurement_unit: measurement_unit_model.MeasurementUnit) -> measurement_unit_model.MeasurementUnit:
        """Delete a measurement unit."""
        db.delete(db_measurement_unit)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

        return db_measurement_unit