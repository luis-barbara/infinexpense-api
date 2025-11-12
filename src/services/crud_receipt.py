# src/services/crud_receipt.py

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from decimal import Decimal

from src.models import receipt as model_receipt
from src.models import receipt_product as model_receipt_product
from src.models import merchant as model_merchant
from src.schemas import receipt as schema_receipt
from . import crud_merchant


# Função para calcular o total de um recibo
def _calculate_receipt_total(db_receipt: model_receipt.Receipt) -> Decimal:
    """
    Calcula o preço total de um recibo: sum(price * quantity) de todos os produtos.
    """
    total = Decimal("0.0")
    if db_receipt.products:
        for item in db_receipt.products:
            total += item.price * item.quantity
    return total.quantize(Decimal("0.01"))


# Read
def get_receipt(db: Session, receipt_id: int) -> Optional[model_receipt.Receipt]:
    """
    Obtém um recibo pelo ID, carregando products e merchant.
    """
    db_receipt = (
        db.query(model_receipt.Receipt)
        .options(
            joinedload(model_receipt.Receipt.products)
            .joinedload(model_receipt_product.Product.product_list),
            joinedload(model_receipt.Receipt.merchant),
        )
        .filter(model_receipt.Receipt.id == receipt_id)
        .first()
    )

    if db_receipt:
        db_receipt.total_price = _calculate_receipt_total(db_receipt)
    return db_receipt


def get_receipts(db: Session, skip: int = 0, limit: int = 100) -> List[model_receipt.Receipt]:
    """
    Obtém recibos com paginação e calcula o total de cada um.
    """
    db_receipts = (
        db.query(model_receipt.Receipt)
        .options(
            joinedload(model_receipt.Receipt.products)
            .joinedload(model_receipt_product.Product.product_list),
            joinedload(model_receipt.Receipt.merchant),
        )
        .order_by(model_receipt.Receipt.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    for db_receipt in db_receipts:
        db_receipt.total_price = _calculate_receipt_total(db_receipt)

    return db_receipts


# Create
def create_receipt(db: Session, receipt_data: schema_receipt.ReceiptCreate) -> model_receipt.Receipt:
    """
    Cria um novo recibo.
    """
    merchant = crud_merchant.get_merchant(db, receipt_data.merchant_id)
    if not merchant:
        raise ValueError(f"Merchant ID '{receipt_data.merchant_id}' not found")

    db_receipt = model_receipt.Receipt(**receipt_data.model_dump())
    db.add(db_receipt)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Database constraint violation while creating receipt")

    db.refresh(db_receipt)

    # Inicializa o total e injeta o merchant carregado
    db_receipt.total_price = Decimal("0.00")
    db_receipt.merchant = merchant
    return db_receipt


# Update
def update_receipt(
    db: Session, db_receipt: model_receipt.Receipt, update_data: schema_receipt.ReceiptUpdate
) -> model_receipt.Receipt:
    """
    Atualiza um recibo.
    """
    update_dict = update_data.model_dump(exclude_unset=True)

    # Valida merchant_id se for alterado
    if "merchant_id" in update_dict:
        merchant = crud_merchant.get_merchant(db, update_dict["merchant_id"])
        if not merchant:
            raise ValueError(f"Merchant ID '{update_dict['merchant_id']}' not found")

    # Aplica os updates
    for key, value in update_dict.items():
        setattr(db_receipt, key, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Database constraint violation while updating receipt")

    db.refresh(db_receipt)

    # Recalcula o total
    db_receipt.total_price = _calculate_receipt_total(db_receipt)
    db.refresh(db_receipt.merchant)
    return db_receipt


# Delete
def delete_receipt(db: Session, db_receipt: model_receipt.Receipt) -> model_receipt.Receipt:
    """
    Deleta um recibo e seus produtos (cascade).
    """
    db_receipt.total_price = _calculate_receipt_total(db_receipt)

    db.delete(db_receipt)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Cannot delete receipt: integrity constraint violation")

    return db_receipt
