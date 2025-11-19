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
    """
    Create a new receipt with the provided details.
    - **merchant_id**: ID of the merchant associated with the receipt
    - **date**: Date of the receipt
    - **barcode**: Optional barcode number for the receipt
    - **products**: List of products associated with the receipt
    Returns the created receipt.
    """
    return ReceiptService.create_receipt(db, receipt)



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
    """
    Retrieve all receipts with optional filtering by:
    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of records to return
    - **merchant_id**: Filter receipts by the associated merchant ID
    - **barcode**: Filter receipts by barcode
    - **start_date** and **end_date**: Filter receipts within a date range
    - **end_date**: Filter receipts up to this date (inclusive)

    Returns a list of receipts matching the criteria.
    """
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
    db:  Session = Depends(get_db)
):
    """
    Retrive a receipt by its unique ID.

    - **receipt_id**: The unique identifier of the receipt to retrieve
    
    Returns the receipt details including:
    - Merchant information
    - Date of the receipt
    - Barcode (if available)
    - List of products associated with the receipt
    """
    return ReceiptService.get_receipt_by_id(db, receipt_id)



@router.get(
    "/{receipt_id}/products",
    response_model=List[ReceiptSchema],
    summary="Retrieve all products associated with a specific receipt"
)
def get_receipts_products(
    receipt_id: int = Path(..., gt=0, description="The ID of the receipt to retrieve products for"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all products associated with a specific receipt.

    - **receipt_id**: The unique identifier of the receipt

    Returns a list of products linked to the specified receipt.
    """
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
    """
    Retrieve a receipt by its barcode.

    - **barcode**: The barcode associated with the receipt

    Returns the receipt details including:
    - Merchant information
    - Date of the receipt
    - Barcode
    - List of products associated with the receipt
    """
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
    """
    Retrieve all receipts associated with a specific merchant.

    - **merchant_id**: The unique identifier of the merchant

    Returns a list of receipts linked to the specified merchant.
    """
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
    """
    Update an existing receipt with the provided details.

    - **receipt_id**: The unique identifier of the receipt to update
    - **merchant_id**: Updated ID of the merchant associated with the receipt
    - **date**: Updated date of the receipt
    - **barcode**: Updated optional barcode number for the receipt
    Returns the updated receipt.
    """
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
    """
    Update all products for a receipt.
    """
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
    """
    Delete a receipt by its unique ID.

    - **receipt_id**: The unique identifier of the receipt to delete

    This operation will remove the receipt and all associated products from the database.
    """
    ReceiptService.delete_receipt(db, receipt_id)
    return None