# src/services/crud_merchant.py

from sqlalchemy.orm import Session
from typing import List, Optional

from src.models import merchant as merchant_model
from src.models.receipt import Receipt
from src.schemas import merchant as merchant_schema


class MerchantService:
    
    # Read
    @staticmethod
    def get_merchant(db: Session, merchant_id: int) -> Optional[merchant_model.Merchant]:
        return db.query(merchant_model.Merchant).filter(
            merchant_model.Merchant.id == merchant_id
        ).first()

    @staticmethod
    def get_merchants(db: Session, skip: int = 0, limit: int = 100) -> List[merchant_model.Merchant]:
        """Get all merchants with pagination"""
        return db.query(merchant_model.Merchant).offset(skip).limit(limit).all()

    # Create
    @staticmethod
    def create_merchant(db: Session, merchant: merchant_schema.MerchantCreate) -> merchant_model.Merchant:
        db_merchant = merchant_model.Merchant(**merchant.dict())
        db.add(db_merchant)
        db.commit()
        db.refresh(db_merchant)
        return db_merchant

    # Update
    @staticmethod
    def update_merchant(db: Session, merchant_id: int, merchant_update: merchant_schema.MerchantUpdate) -> Optional[merchant_model.Merchant]:
        db_merchant = db.query(merchant_model.Merchant).filter(
            merchant_model.Merchant.id == merchant_id
        ).first()
        
        if db_merchant:
            update_data = merchant_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_merchant, key, value)
            db.commit()
            db.refresh(db_merchant)
        
        return db_merchant

    # Delete
    @staticmethod
    def delete_merchant(db: Session, merchant_id: int) -> bool:
        try:
            db_merchant = db.query(merchant_model.Merchant).filter(
                merchant_model.Merchant.id == merchant_id
            ).first()
            
            if not db_merchant:
                return False
            
            # Check if merchant is associated with any receipts
            associated_receipts = db.query(Receipt).filter(
                Receipt.merchant_id == merchant_id
            ).count()
            
            if associated_receipts > 0:
                raise Exception(f"Cannot delete merchant. It is associated with {associated_receipts} receipt(s).")
            
            # Delete the merchant
            db.delete(db_merchant)
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            raise e