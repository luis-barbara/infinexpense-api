from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from src.models import receipt_product as product_item_model
from src.models import receipt as receipt_model
from src.models import product as product_list_model
from src.schemas import product as product_item_schema

from .crud_receipt import ReceiptService
from .crud_product_list import ProductListService


class ReceiptProductService:
    @staticmethod
    def get_product_item(db: Session, product_item_id: int) -> Optional[product_item_model.Product]:
        """Get a product item by ID."""
        return (
            db.query(product_item_model.Product)
            .filter(product_item_model.Product.id == product_item_id)
            .first()
        )

    @staticmethod
    def get_product_items_for_receipt(db: Session, receipt_id: int, skip: int = 0, limit: int = 100) -> List[product_item_model.Product]:
        """Get all product items for a receipt with pagination."""
        return (
            db.query(product_item_model.Product)
            .filter(product_item_model.Product.receipt_id == receipt_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create_product_item_for_receipt(db: Session, receipt_id: int, product_item_data: product_item_schema.ProductCreate) -> product_item_model.Product:
        """Create a product item for a receipt."""
        db_receipt = ReceiptService.get_receipt_by_id(db, receipt_id)
        if not db_receipt:
            raise ValueError(f"Receipt ID '{receipt_id}' not found")

        # 2. Verificar se o produto da lista existe
        db_product_list = ProductListService.get_product_list(db, product_item_data.product_list_id)
        if not db_product_list:
            raise ValueError(
                f"ProductList ID '{product_item_data.product_list_id}' not found"
            )

        # Criar objeto Product (receipt_id vem da rota)
        db_product_item = product_item_model.Product(**product_item_data.model_dump(), receipt_id=receipt_id)
        db.add(db_product_item)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError("Database constraint violation")

        db.refresh(db_product_item)
        return db_product_item


    @staticmethod
    def update_product_item(db: Session, db_product_item: product_item_model.Product, update_data: product_item_schema.ProductUpdate) -> product_item_model.Product:
        """Update a product item."""
        update_dict = update_data.model_dump(exclude_unset=True)
        if "product_list_id" in update_dict:
            db_product_list = ProductListService.get_product_list(db, update_dict["product_list_id"])
            if not db_product_list:
                raise ValueError(
                    f"ProductList ID '{update_dict['product_list_id']}' not found"
                )

        # Aplicar alterações
        for key, value in update_dict.items():
            setattr(db_product_item, key, value)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError("Database constraint violation")

        db.refresh(db_product_item)
        return db_product_item


    @staticmethod
    def delete_product_item(db: Session, db_product_item: product_item_model.Product) -> product_item_model.Product:
        """Delete a product item."""
        db.delete(db_product_item)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError("Cannot delete: Integrity constraint violation")

        return db_product_item