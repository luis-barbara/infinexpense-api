# src/services/crud_receipt.py

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from decimal import Decimal
from datetime import date

from src.models import receipt as model_receipt
from src.models import receipt_product as model_receipt_product
from src.models import merchant as model_merchant
from src.schemas import receipt as schema_receipt
from . import crud_merchant


class ReceiptService:
    @staticmethod
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
    @staticmethod
    def get_receipts(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        merchant_id: Optional[int] = None,
        barcode: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[model_receipt.Receipt]:
        """
        Obtém recibos com paginação e filtros opcionais.
        Calcula o total (price * quantity) de cada recibo.
        """
        query = (
            db.query(model_receipt.Receipt)
            .options(
                joinedload(model_receipt.Receipt.products)
                .joinedload(model_receipt_product.Product.product_list),
                joinedload(model_receipt.Receipt.merchant),
            )
        )

        # Filtros opcionais
        if merchant_id is not None:
            query = query.filter(model_receipt.Receipt.merchant_id == merchant_id)
        if barcode is not None:
            query = query.filter(model_receipt.Receipt.barcode == barcode)
        if start_date is not None:
            query = query.filter(model_receipt.Receipt.purchase_date >= start_date)
        if end_date is not None:
            query = query.filter(model_receipt.Receipt.purchase_date <= end_date)

        db_receipts = (
            query.order_by(model_receipt.Receipt.purchase_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        for db_receipt in db_receipts:
            db_receipt.total_price = ReceiptService._calculate_receipt_total(db_receipt)

        return db_receipts

    # Create
    @staticmethod
    def create_receipt(
        db: Session, receipt_data: schema_receipt.ReceiptCreate
    ) -> model_receipt.Receipt:
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

        db_receipt.total_price = Decimal("0.00")
        db_receipt.merchant = merchant
        return db_receipt

    # Update
    @staticmethod
    def update_receipt(
        db: Session,
        db_receipt: model_receipt.Receipt,
        update_data: schema_receipt.ReceiptUpdate,
    ) -> model_receipt.Receipt:
        """
        Atualiza um recibo.
        """
        update_dict = update_data.model_dump(exclude_unset=True)

        if "merchant_id" in update_dict:
            merchant = crud_merchant.get_merchant(db, update_dict["merchant_id"])
            if not merchant:
                raise ValueError(f"Merchant ID '{update_dict['merchant_id']}' not found")

        for key, value in update_dict.items():
            setattr(db_receipt, key, value)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError("Database constraint violation while updating receipt")

        db.refresh(db_receipt)

        db_receipt.total_price = ReceiptService._calculate_receipt_total(db_receipt)
        db.refresh(db_receipt.merchant)
        return db_receipt

    # Delete
    @staticmethod
    def delete_receipt(
        db: Session, db_receipt: model_receipt.Receipt
    ) -> model_receipt.Receipt:
        """
        Deleta um recibo e seus produtos (cascade).
        """
        db_receipt.total_price = ReceiptService._calculate_receipt_total(db_receipt)

        db.delete(db_receipt)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError("Cannot delete receipt: integrity constraint violation")

        return db_receipt
