# src/services/crud_receipt_product.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from src.models import receipt_product as product_item_model
from src.models import receipt as receipt_model
from src.models import product as product_list_model
from src.schemas import product as product_item_schema

from . import crud_receipt
from . import crud_product_list



# Read
def get_product_item(db: Session, product_item_id: int) -> Optional[product_item_model.Product]:
    """
    Obtém um item de produto (num recibo) pelo ID.
    """
    return (
        db.query(product_item_model.Product)
        .filter(product_item_model.Product.id == product_item_id)
        .first()
    )


def get_product_items_for_receipt(db: Session, receipt_id: int, skip: int = 0, limit: int = 100) -> List[product_item_model.Product]:
    """
    Obtém todos os itens de produto pertencentes a um recibo.
    """
    return (
        db.query(product_item_model.Product)
        .filter(product_item_model.Product.receipt_id == receipt_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# Create
def create_product_item_for_receipt(db: Session, receipt_id: int, product_item_data: product_item_schema.ProductCreate) -> product_item_model.Product:
    """
    Cria um item de produto associado a um recibo.
    Verifica se o recibo e o produto da lista existem.
    """

    # 1. Verificar se o recibo existe
    db_receipt = crud_receipt.get_receipt(db, receipt_id)
    if not db_receipt:
        raise ValueError(f"Receipt ID '{receipt_id}' not found")

    # 2. Verificar se o produto da lista existe
    db_product_list = crud_product_list.get_product_list(db, product_item_data.product_list_id)
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


# Update
def update_product_item(db: Session, db_product_item: product_item_model.Product, update_data: product_item_schema.ProductUpdate) -> product_item_model.Product:
    """
    Atualiza um item de produto de um recibo.
    """

    update_dict = update_data.model_dump(exclude_unset=True)

    # Validar novo product_list_id, se presente
    if "product_list_id" in update_dict:
        db_product_list = crud_product_list.get_product_list(db, update_dict["product_list_id"])
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


# Delete
def delete_product_item(db: Session, db_product_item: product_item_model.Product) -> product_item_model.Product:
    """
    Apaga um item de produto pertencente a um recibo.
    """
    db.delete(db_product_item)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Cannot delete: Integrity constraint violation")

    return db_product_item
