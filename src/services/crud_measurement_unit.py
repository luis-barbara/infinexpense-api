# src/services/crud_measurement_unit.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
import logging

from src.models import measurement_unit as measurement_unit_model
from src.schemas import measurement_unit as measurement_unit_schema


logger = logging.getLogger(__name__)

class MeasurementUnitService:
    # Read 
    def get_measurement_unit(db: Session, measurement_unit_id: int) -> Optional[measurement_unit_model.MeasurementUnit]:
        """
        Obtem uma unidade de medida através do ID
        """
        return db.query(measurement_unit_model.MeasurementUnit).filter(
            measurement_unit_model.MeasurementUnit.id == measurement_unit_id).first()


    def get_measurement_units(db: Session, skip: int = 0, limit: int = 100) -> List[measurement_unit_model.MeasurementUnit]:
        """
        Obtem uma lista de unidades de medida com paginação.
        """
        logger.info(f"Fetching measurement units (skip={skip}, limit={limit})")
        
        try:
            units = (
                db.query(measurement_unit_model.MeasurementUnit)
                .offset(skip)
                .limit(limit)
                .all()
            )
            logger.info(f"Returning {len(units)} measurement units")
            return units
        except Exception as e:
            logger.error(f"Error fetching measurement units: {str(e)}", exc_info=True)
            raise


    # Create
    def create_measurement_unit(db: Session, measurement_unit_data: measurement_unit_schema.MeasurementUnitCreate) -> measurement_unit_model.MeasurementUnit:
        """
        Cria uma nova unidade de medida.
        """
        logger.info(f"Creating measurement unit: {measurement_unit_data.name}")

        # Verificar se existem duplicados
        existing = db.query(measurement_unit_model.MeasurementUnit).filter_by(name=measurement_unit_data.name).first()
        if existing:
            logger.warning(f"Duplicate measurement unit name: {measurement_unit_data.name}")
            raise ValueError(f"Measurement Unit '{measurement_unit_data.name}' already exists.")

        db_measurement_unit = measurement_unit_model.MeasurementUnit(**measurement_unit_data.model_dump())
        db.add(db_measurement_unit)

        try:
            db.commit()
            db.refresh(db_measurement_unit)
            logger.info(f"Measurement unit created successfully: {db_measurement_unit.name} (id={db_measurement_unit.id})")
            return db_measurement_unit
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Error creating measurement unit: {str(e)}", exc_info=True)
            raise



    # Update
    def update_measurement_unit(db: Session, db_measurement_unit: measurement_unit_model.MeasurementUnit, update_data: measurement_unit_schema.MeasurementUnitUpdate) -> measurement_unit_model.MeasurementUnit:
        """
        Atualiza uma unidade de medida existente.
        """
        logger.info(f"Updating measurement unit: id={db_measurement_unit.id}")
        update_dict = update_data.model_dump(exclude_unset=True)


        # Verificar se existe o nome duplicado
        if 'name' in update_dict:
            existing = db.query(measurement_unit_model.MeasurementUnit).filter_by(name=update_dict['name']).first()
            if existing and existing.id != db_measurement_unit.id:
                logger.warning(f"Duplicate measurement unit name during update: {update_dict['name']}")
                raise ValueError(f"Measurement Unit '{update_dict['name']}' already exists.")

        for key, value in update_dict.items():
            setattr(db_measurement_unit, key, value)

        try:
            db.commit()
            db.refresh(db_measurement_unit)
            logger.info(f"Measurement unit updated successfully: id={db_measurement_unit.id}")
            return db_measurement_unit
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Error updating measurement unit {db_measurement_unit.id}: {str(e)}", exc_info=True)
            raise



    # Delete
    def delete_measurement_unit(db: Session, db_measurement_unit: measurement_unit_model.MeasurementUnit) -> measurement_unit_model.MeasurementUnit:
        """
        Apaga uma unidade de medida.
        """
        logger.info(f"Deleting measurement unit: id={db_measurement_unit.id}")

        db.delete(db_measurement_unit)

        try:
            db.commit()
            logger.info(f"Measurement unit deleted successfully: id={db_measurement_unit.id}")
            return db_measurement_unit
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Error deleting measurement unit {db_measurement_unit.id}: {str(e)}", exc_info=True)
            raise