# src/services/crud_receipt.py
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status

from src.models.receipt import Receipt
from src.models.product import Product
from src.schemas.receipt import ReceiptCreate, ReceiptUpdate


class ReceiptService:
    
    @staticmethod
    def create_receipt(db: Session, receipt_data: ReceiptCreate) -> Receipt:
        """Cria um novo recibo"""
        # Criar o recibo
        db_receipt = Receipt(
            merchant_id=receipt_data.merchant_id,
            date=receipt_data.date,
            barcode=receipt_data.barcode
        )
        db.add(db_receipt)
        db.commit()
        db.refresh(db_receipt)
        
        # Adicionar produtos se existirem
        if receipt_data.products:
            for product_data in receipt_data.products:
                product = Product(
                    receipt_id=db_receipt.id,
                    **product_data.dict()
                )
                db.add(product)
            db.commit()
            db.refresh(db_receipt)
        
        return db_receipt
    
    @staticmethod
    def get_receipts(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        merchant_id: Optional[int] = None,
        barcode: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Receipt]:
        """Obtém recibos com filtros opcionais"""
        query = db.query(Receipt)
        
        if merchant_id:
            query = query.filter(Receipt.merchant_id == merchant_id)
        if barcode:
            query = query.filter(Receipt.barcode == barcode)
        if start_date:
            query = query.filter(Receipt.date >= start_date)
        if end_date:
            query = query.filter(Receipt.date <= end_date)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_receipt_by_id(db: Session, receipt_id: int) -> Receipt:
        """Obtém um recibo pelo ID"""
        receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Receipt with id {receipt_id} not found"
            )
        return receipt
    
    @staticmethod
    def get_receipt_by_barcode(db: Session, barcode: str) -> Receipt:
        """Obtém um recibo pelo barcode"""
        receipt = db.query(Receipt).filter(Receipt.barcode == barcode).first()
        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Receipt with barcode {barcode} not found"
            )
        return receipt
    
    @staticmethod
    def get_receipt_products(db: Session, receipt_id: int) -> List[Product]:
        """Obtém todos os produtos de um recibo"""
        receipt = ReceiptService.get_receipt_by_id(db, receipt_id)
        return receipt.products
    
    @staticmethod
    def get_receipts_by_merchant(
        db: Session, 
        merchant_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Receipt]:
        """Obtém todos os recibos de um merchant"""
        return db.query(Receipt)\
            .filter(Receipt.merchant_id == merchant_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    @staticmethod
    def update_receipt(
        db: Session, 
        receipt_id: int, 
        receipt_update: ReceiptUpdate
    ) -> Receipt:
        """Atualiza um recibo"""
        receipt = ReceiptService.get_receipt_by_id(db, receipt_id)
        
        update_data = receipt_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(receipt, field, value)
        
        db.commit()
        db.refresh(receipt)
        return receipt
    
    @staticmethod
    def delete_receipt(db: Session, receipt_id: int) -> None:
        """Remove um recibo"""
        receipt = ReceiptService.get_receipt_by_id(db, receipt_id)
        db.delete(receipt)
        db.commit()