from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException, status

from src.models import product as product_list_model
from src.models.receipt_product import Product  # Change ReceiptProduct to Product
from src.schemas import product as product_list_schema

from . import crud_measurement_unit
from . import crud_category


class ProductListService:
    @staticmethod
    def get_product_list(db: Session, product_list_id: int) -> Optional[product_list_model.ProductList]:
        """Get a product by ID."""
        return db.query(product_list_model.ProductList).filter(
            product_list_model.ProductList.id == product_list_id
        ).first()

    @staticmethod
    def get_product_lists(db: Session, skip: int = 0, limit: int = 100) -> List[product_list_model.ProductList]:
        """Get all products with pagination."""
        return db.query(product_list_model.ProductList).offset(skip).limit(limit).all()

    @staticmethod
    def get_product_by_barcode(db: Session, barcode: str) -> Optional[product_list_model.ProductList]:
        """Get a product by barcode."""
        return db.query(product_list_model.ProductList).filter(
            product_list_model.ProductList.barcode == barcode
        ).first()

    @staticmethod
    def get_product_by_name(db: Session, name: str) -> Optional[product_list_model.ProductList]:
        """Get a product by name."""
        return db.query(product_list_model.ProductList).filter(
            product_list_model.ProductList.name == name
        ).first()

    @staticmethod
    def create_product_list(db: Session, product: product_list_schema.ProductListCreate):
        """Create a new product."""
        db_product = product_list_model.ProductList(**product.model_dump())
        db.add(db_product)
        try:
            db.commit()
            db.refresh(db_product)
            return db_product
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Product with name '{product.name}' already exists"
            )

    @staticmethod
    def update_product_list(db: Session, product_id: int, product_update: product_list_schema.ProductListUpdate) -> Optional[product_list_model.ProductList]:
        """Update a product."""
        db_product = db.query(product_list_model.ProductList).filter(
            product_list_model.ProductList.id == product_id
        ).first()
        
        if db_product:
            update_data = product_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_product, key, value)
            db.commit()
            db.refresh(db_product)
        
        return db_product

    @staticmethod
    def delete_product_list(db: Session, product_id: int) -> bool:
        """Delete a product by ID."""
        try:
            db_product_list = db.query(product_list_model.ProductList).filter(
                product_list_model.ProductList.id == product_id
            ).first()
            
            if not db_product_list:
                return False
            
            # Check if product is associated with any receipts
            associated_products = db.query(Product).filter(
                Product.product_list_id == product_id
            ).count()
            
            if associated_products > 0:
                raise Exception(f"Cannot delete product. It is associated with {associated_products} receipt(s).")
            
            # Delete the product_list
            db.delete(db_product_list)
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            raise e