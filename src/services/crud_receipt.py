# src/services/crud_receipt.py

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from decimal import Decimal
from datetime import date
from pydantic import BaseModel, Field

from src.models import receipt as model_receipt
from src.models import receipt_product as model_receipt_product
from src.models import merchant as model_merchant
from src.schemas import receipt as schema_receipt
from src.services.crud_merchant import MerchantService


class ReceiptBase(BaseModel):
    merchant_id: int
    purchase_date: date
    barcode: str | None = Field(default=None, max_length=20, description="Barcode from receipt (optional)")
    notes: str | None = Field(default=None, max_length=500, description="Notes about the receipt (optional)")


class ReceiptService:
    @staticmethod
    def _calculate_receipt_total(receipt: model_receipt.Receipt) -> Decimal:
        """
        Calculate total price of all products in receipt.
        """
        if not receipt.products:
            return Decimal("0.00")
        
        total = sum(
            Decimal(str(product.price)) * Decimal(str(product.quantity))
            for product in receipt.products
        )
        return total

    # Read - Get all receipts
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
                joinedload(model_receipt.Receipt.products),
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
            if db_receipt.products is None:
                db_receipt.products = []
            db_receipt.total_price = ReceiptService._calculate_receipt_total(db_receipt)

        return db_receipts

    # Read - Get receipt by ID
    @staticmethod
    def get_receipt_by_id(db: Session, receipt_id: int) -> model_receipt.Receipt:
        """
        Obtém um recibo específico pelo ID com produtos associados.
        """
        db_receipt = (
            db.query(model_receipt.Receipt)
            .options(
                joinedload(model_receipt.Receipt.products),
                joinedload(model_receipt.Receipt.merchant),
            )
            .filter(model_receipt.Receipt.id == receipt_id)
            .first()
        )

        if not db_receipt:
            raise ValueError(f"Receipt with ID '{receipt_id}' not found")

        # Garante que os produtos estão carregados
        if db_receipt.products is None:
            db_receipt.products = []

        db_receipt.total_price = ReceiptService._calculate_receipt_total(db_receipt)
        return db_receipt

    # Read - Get receipt products
    @staticmethod
    def get_receipt_products(db: Session, receipt_id: int) -> List[model_receipt_product.Product]:
        """
        Obtém todos os produtos de um recibo específico.
        """
        db_receipt = (
            db.query(model_receipt.Receipt)
            .options(joinedload(model_receipt.Receipt.products))
            .filter(model_receipt.Receipt.id == receipt_id)
            .first()
        )

        if not db_receipt:
            raise ValueError(f"Receipt with ID '{receipt_id}' not found")

        return db_receipt.products or []

    # Read - Get receipt by barcode
    @staticmethod
    def get_receipt_by_barcode(db: Session, barcode: str) -> model_receipt.Receipt:
        """
        Obtém um recibo pelo seu barcode.
        """
        db_receipt = (
            db.query(model_receipt.Receipt)
            .options(
                joinedload(model_receipt.Receipt.products)
                .joinedload(model_receipt_product.Product.product_list),
                joinedload(model_receipt.Receipt.merchant),
            )
            .filter(model_receipt.Receipt.barcode == barcode)
            .first()
        )

        if not db_receipt:
            raise ValueError(f"Receipt with barcode '{barcode}' not found")

        db_receipt.total_price = ReceiptService._calculate_receipt_total(db_receipt)
        return db_receipt

    # Read - Get receipts by merchant
    @staticmethod
    def get_receipts_by_merchant(
        db: Session, merchant_id: int, skip: int = 0, limit: int = 100
    ) -> List[model_receipt.Receipt]:
        """
        Obtém todos os recibos de um comerciante específico.
        """
        db_receipts = (
            db.query(model_receipt.Receipt)
            .options(
                joinedload(model_receipt.Receipt.products)
                .joinedload(model_receipt_product.Product.product_list),
                joinedload(model_receipt.Receipt.merchant),
            )
            .filter(model_receipt.Receipt.merchant_id == merchant_id)
            .order_by(model_receipt.Receipt.purchase_date.desc())
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
        merchant = MerchantService.get_merchant(db, receipt_data.merchant_id)
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
        receipt_id: int,
        update_data: schema_receipt.ReceiptUpdate,
    ) -> model_receipt.Receipt:
        """
        Atualiza um recibo.
        """
        db_receipt = db.query(model_receipt.Receipt).filter(
            model_receipt.Receipt.id == receipt_id
        ).first()

        if not db_receipt:
            raise ValueError(f"Receipt with ID '{receipt_id}' not found")

        update_dict = update_data.model_dump(exclude_unset=True)

        if "merchant_id" in update_dict:
            merchant = MerchantService.get_merchant(db, update_dict["merchant_id"])
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
        db.refresh(db_receipt.merchant)

        db_receipt.total_price = ReceiptService._calculate_receipt_total(db_receipt)
        return db_receipt

    # Update - Update receipt products
    @staticmethod
    def update_receipt_products(
        db: Session,
        receipt_id: int,
        products_data: List[dict]
    ) -> model_receipt.Receipt:
        """
        Updates all products for a receipt.
        Removes old products and creates new ones.
        """
        db_receipt = db.query(model_receipt.Receipt).filter(
            model_receipt.Receipt.id == receipt_id
        ).first()

        if not db_receipt:
            raise ValueError(f"Receipt with ID '{receipt_id}' not found")

        try:
            # Delete all existing products for this receipt
            db.query(model_receipt_product.Product).filter(
                model_receipt_product.Product.receipt_id == receipt_id
            ).delete()

            # Create new products
            for product_data in products_data:
                new_product = model_receipt_product.Product(
                    receipt_id=receipt_id,
                    product_list_id=product_data.get('product_list_id'),
                    price=Decimal(str(product_data.get('price', 0))),
                    quantity=Decimal(str(product_data.get('quantity', 1)))
                )
                db.add(new_product)

            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError("Database constraint violation while updating products")

        db.refresh(db_receipt)
        
        # Calculate and set total price
        db_receipt.total_price = ReceiptService._calculate_receipt_total(db_receipt)
        
        return db_receipt

    # Delete
    @staticmethod
    def delete_receipt(db: Session, receipt_id: int) -> None:
        """
        Deleta um recibo e seus produtos (cascade).
        """
        db_receipt = db.query(model_receipt.Receipt).filter(
            model_receipt.Receipt.id == receipt_id
        ).first()

        if not db_receipt:
            raise ValueError(f"Receipt with ID '{receipt_id}' not found")

        db.delete(db_receipt)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError("Cannot delete receipt: integrity constraint violation")
