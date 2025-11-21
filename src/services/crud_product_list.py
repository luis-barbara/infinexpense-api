# src/services/crud_product_list.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException, status
import logging

from src.models import product as product_list_model
from src.models.receipt_product import Product  # Change ReceiptProduct to Product
from src.schemas import product as product_list_schema

from . import crud_measurement_unit
from . import crud_category


logger = logging.getLogger(__name__)

class ProductListService:
    # Read
    @staticmethod
    def get_product_list(db: Session, product_list_id: int) -> Optional[product_list_model.ProductList]:
        return db.query(product_list_model.ProductList).filter(
            product_list_model.ProductList.id == product_list_id
        ).first()

    @staticmethod
    def get_product_lists(db: Session, skip: int = 0, limit: int = 100) -> List[product_list_model.ProductList]:
        """Get all product lists with pagination"""
        logger.info(f"Fetching product lists (skip={skip}, limit={limit})")
        
        try:
            products = db.query(product_list_model.ProductList).offset(skip).limit(limit).all()
            logger.info(f"Returning {len(products)} product lists")
            return products
        except Exception as e:
            logger.error(f"Error fetching product lists: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def get_product_by_barcode(db: Session, barcode: str) -> Optional[product_list_model.ProductList]:
        return db.query(product_list_model.ProductList).filter(
            product_list_model.ProductList.barcode == barcode
        ).first()

    @staticmethod
    def get_product_by_name(db: Session, name: str) -> Optional[product_list_model.ProductList]:
        return db.query(product_list_model.ProductList).filter(
            product_list_model.ProductList.name == name
        ).first()

    # Create
    @staticmethod
    def create_product_list(db: Session, product: product_list_schema.ProductListCreate):  # CORRIGE AQUI
        logger.info(f"Creating product list: {product.name}")
        
        db_product = product_list_model.ProductList(**product.model_dump())
        db.add(db_product)

        try:
            db.commit()
            db.refresh(db_product)
            logger.info(f"Product list created successfully: {db_product.name} (id={db_product.id})")
            return db_product
        except IntegrityError as e:
            db.rollback()
            logger.warning(f"Duplicate product list name: {product.name}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Product with name '{product.name}' already exists"
            )

    # Update
    @staticmethod
    def update_product_list(db: Session, product_id: int, product_update: product_list_schema.ProductListUpdate) -> Optional[product_list_model.ProductList]:
        logger.info(f"Updating product list: id={product_id}")
        
        db_product = db.query(product_list_model.ProductList).filter(
            product_list_model.ProductList.id == product_id
        ).first()
        
        if db_product:
            update_data = product_update.model_dump(exclude_unset=True)
            
            for key, value in update_data.items():
                setattr(db_product, key, value)

            try:
                db.commit()
                db.refresh(db_product)
                logger.info(f"Product list updated successfully: id={product_id}")
                return db_product
            except Exception as e:
                db.rollback()
                logger.error(f"Error updating product list {product_id}: {str(e)}", exc_info=True)
                raise
        else:
            logger.warning(f"Product list not found for update: id={product_id}")
            return None


    # Delete
    @staticmethod
    def delete_product_list(db: Session, product_id: int) -> bool:
        logger.info(f"Deleting product list: id={product_id}")
        
        try:
            db_product_list = db.query(product_list_model.ProductList).filter(
                product_list_model.ProductList.id == product_id
            ).first()
            
            if not db_product_list:
                logger.warning(f"Product list not found for deletion: id={product_id}")
                return False
            
            # Check if product is associated with any receipts
            associated_products = db.query(Product).filter(
                Product.product_list_id == product_id
            ).count()
            
            if associated_products > 0:
                logger.warning(f"Cannot delete product list {product_id}: associated with {associated_products} receipt(s)")
                raise Exception(f"Cannot delete product. It is associated with {associated_products} receipt(s).")
            
            # Delete the product_list
            db.delete(db_product_list)
            db.commit()
            logger.info(f"Product list deleted successfully: id={product_id}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting product list {product_id}: {str(e)}", exc_info=True)
            raise e