# src/routers/receipts.py

from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, status, Query, Path, HTTPException
from sqlalchemy.orm import Session
from fastapi import Body

from src.database import get_db
from src.schemas.receipt import (
    ReceiptCreate, 
    ReceiptUpdate, 
    Receipt as ReceiptSchema
)
from src.services.crud_receipt import ReceiptService

router = APIRouter(
    prefix="/receipts",
    tags=["Receipts"]
)


@router.post(
    "/", 
    response_model=ReceiptSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new receipt"
)
def create_receipt(
    receipt: ReceiptCreate,
    db: Session = Depends(get_db)
):
    """Create a new receipt."""
    try:
        return ReceiptService.create_receipt(db, receipt)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=List[ReceiptSchema],
    summary="Retrieve all receipts with optional filtering"
)
def get_receipt_by_filter(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    merchant_id: Optional[int] = Query(None, description="Filter by merchant ID"),
    barcode: Optional[str] = Query(None, description="Filter by receipt barcode"),
    start_date: Optional[date] = Query(None, description="Filter receipts from this date (inclusive)"),
    end_date: Optional[date] = Query(None, description="Filter receipts up to this date (inclusive)"),
    db: Session = Depends(get_db),
):
    """Get all receipts with optional filtering and pagination."""
    return ReceiptService.get_receipts(
        db=db, 
        skip=skip, 
        limit=limit, 
        merchant_id=merchant_id, 
        barcode=barcode, 
        start_date=start_date, 
        end_date=end_date
    )


@router.get(
    "/{receipt_id}",
    response_model=ReceiptSchema,
    summary="Retrieve a receipt by its ID"
)
def get_receipt_by_id(
    receipt_id: int = Path(..., gt=0, description="The ID of the receipt to retrieve"),
    db: Session = Depends(get_db)
):
    """Get a single receipt by ID."""
    try:
        return ReceiptService.get_receipt_by_id(db, receipt_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found" 
        )


@router.get(
    "/{receipt_id}/products",
    response_model=List[ReceiptSchema],
    summary="Retrieve all products associated with a specific receipt"
)
def get_receipts_products(
    receipt_id: int = Path(..., gt=0, description="The ID of the receipt to retrieve products for"),
    db: Session = Depends(get_db)
):
    """Get all products for a receipt."""
    return ReceiptService.get_receipt_products(db, receipt_id)



@router.get(
    "/barcode/{barcode}",
    response_model=ReceiptSchema,
    summary="Retrieve a receipt by its barcode"
)
def get_receipt_by_barcode(
    barcode: str = Path(..., description="The barcode of the receipt to retrieve"),
    db: Session = Depends(get_db)
):
    """Get a receipt by barcode."""
    return ReceiptService.get_receipt_by_barcode(db, barcode)



@router.get(
    "/merchant/{merchant_id}",
    response_model=List[ReceiptSchema],
    summary="Retrieve all receipts for a specific merchant"
)
def get_receipts_by_merchant(
    merchant_id: int = Path(..., gt=0, description="The ID of the merchant to retrieve receipts for"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """Get all receipts for a merchant."""
    return ReceiptService.get_receipts_by_merchant(db, merchant_id)



@router.put(
    "/{receipt_id}",
    response_model=ReceiptSchema,
    summary="Update an existing receipt by its ID"
)
def update_receipt(
    receipt_id: int = Path(..., gt=0, description="The ID of the receipt to update"),
    receipt_update: ReceiptUpdate = ...,
    db: Session = Depends(get_db)
):
    """Update a receipt by ID."""
    return ReceiptService.update_receipt(db, receipt_id, receipt_update)

@router.put(
    "/{receipt_id}/products",
    response_model=ReceiptSchema,
    summary="Update products for a receipt"
)
def update_receipt_products(
    receipt_id: int = Path(..., gt=0),
    products_data: dict = Body(...),
    db: Session = Depends(get_db)
):
    """Update all products for a receipt."""
    return ReceiptService.update_receipt_products(db, receipt_id, products_data.get("products", []))

@router.delete(
    "/{receipt_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a receipt by its ID"
)
def delete_receipt(
    receipt_id: int = Path(..., gt=0, description="The ID of the receipt to delete"),
    db: Session = Depends(get_db)
):
    """Delete a receipt by ID."""
    ReceiptService.delete_receipt(db, receipt_id)
    return None