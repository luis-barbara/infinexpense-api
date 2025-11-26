from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from src.models import merchant as merchant_model
from src.models.receipt import Receipt
from src.schemas import merchant as merchant_schema


logger = logging.getLogger(__name__)

class MerchantService:
    @staticmethod
    def get_merchant(db: Session, merchant_id: int) -> Optional[merchant_model.Merchant]:
        """Get a merchant by ID."""
        return db.query(merchant_model.Merchant).filter(
            merchant_model.Merchant.id == merchant_id
        ).first()

    @staticmethod
    def get_merchants(db: Session, skip: int = 0, limit: int = 100) -> List[merchant_model.Merchant]:
        """Get all merchants with pagination"""
        logger.info(f"Fetching merchants (skip={skip}, limit={limit})")
        
        try:
            merchants = db.query(merchant_model.Merchant).offset(skip).limit(limit).all()
            logger.info(f"Returning {len(merchants)} merchants")
            return merchants
        except Exception as e:
            logger.error(f"Error fetching merchants: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def create_merchant(db: Session, merchant: merchant_schema.MerchantCreate) -> merchant_model.Merchant:
        logger.info(f"Creating merchant: {merchant.name}")
        
        db_merchant = merchant_model.Merchant(**merchant.model_dump())
        db.add(db_merchant)

        try:
            db.commit()
            db.refresh(db_merchant)
            logger.info(f"Merchant created successfully: {db_merchant.name} (id={db_merchant.id})")
            return db_merchant
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating merchant: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def update_merchant(db: Session, merchant_id: int, merchant_update: merchant_schema.MerchantUpdate) -> Optional[merchant_model.Merchant]:
        logger.info(f"Updating merchant: id={merchant_id}")
        
        db_merchant = db.query(merchant_model.Merchant).filter(
            merchant_model.Merchant.id == merchant_id
        ).first()
        
        if db_merchant:
            update_data = merchant_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_merchant, key, value)
            try:
                db.commit()
                db.refresh(db_merchant)
                logger.info(f"Merchant updated successfully: id={merchant_id}")
                return db_merchant
            except Exception as e:
                db.rollback()
                logger.error(f"Error updating merchant {merchant_id}: {str(e)}", exc_info=True)
                raise
        else:
            logger.warning(f"Merchant not found for update: id={merchant_id}")
            return None

    @staticmethod
    def delete_merchant(db: Session, merchant_id: int) -> bool:
        logger.info(f"Deleting merchant: id={merchant_id}")
        
        try:
            db_merchant = db.query(merchant_model.Merchant).filter(
                merchant_model.Merchant.id == merchant_id
            ).first()
            
            if not db_merchant:
                logger.warning(f"Merchant not found for deletion: id={merchant_id}")
                return False
            
            # Check if merchant is associated with any receipts
            associated_receipts = db.query(Receipt).filter(
                Receipt.merchant_id == merchant_id
            ).count()
            
            if associated_receipts > 0:
                logger.warning(f"Cannot delete merchant {merchant_id}: associated with {associated_receipts} receipt(s)")
                raise Exception(f"Cannot delete merchant. It is associated with {associated_receipts} receipt(s).")
            
            # Delete the merchant
            db.delete(db_merchant)
            db.commit()
            logger.info(f"Merchant deleted successfully: id={merchant_id}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting merchant {merchant_id}: {str(e)}", exc_info=True)
            raise e
