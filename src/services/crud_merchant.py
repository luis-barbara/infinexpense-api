# src/services/crud_merchant.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from src.models import merchant as merchant_model
from src.schemas import merchant as merchant_schema


# Read 
def get_merchant(db: Session, merchant_id: int) -> Optional[merchant_model.Merchant]:
    """
    Obtem um supermercado através do ID
    """
    return db.query(merchant_model.Merchant).filter(
        merchant_model.Merchant.id == merchant_id).first()


def get_merchants(db: Session, skip: int = 0, limit: int = 100) -> List[merchant_model.Merchant]:
    """
    Obtem uma lista de supermercados com paginação.
    """
    return (
    db.query(merchant_model.Merchant)
    .offset(skip)
    .limit(limit)
    .all()
    )


# Create
def create_merchant(db: Session, merchant_data: merchant_schema.MerchantCreate) -> merchant_model.Merchant:
    """
    Cria um novo supermercado.
    """
    # Verificar se existem duplicados
    existing = db.query(merchant_model.Merchant).filter_by(name=merchant_data.name).first()
    if existing:
        raise ValueError(f"Merchant '{merchant_data.name}' already exists.")

    db_merchant = merchant_model.Merchant(**merchant_data.model_dump())
    db.add(db_merchant)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(db_merchant)
    return db_merchant



# Update
def update_merchant(db: Session, db_merchant: merchant_model.Merchant, update_data: merchant_schema.MerchantUpdate) -> merchant_model.Merchant:
    """
    Atualiza um supermercado existente.
    """
    update_dict = update_data.model_dump(exclude_unset=True)


    # Verificar se existe o nome duplicado
    if 'name' in update_dict:
        existing = db.query(merchant_model.Merchant).filter_by(name=update_dict['name']).first()
        if existing and existing.id != db_merchant.id:
            raise ValueError(f"Merchant '{update_dict['name']}' already exists.")

    for key, value in update_dict.items():
        setattr(db_merchant, key, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(db_merchant)
    return db_merchant



# Delete
def delete_merchant(db: Session, db_merchant: merchant_model.Merchant) -> merchant_model.Merchant:
    """
    Apaga um supermercado.
    """
    db.delete(db_merchant)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    return db_merchant