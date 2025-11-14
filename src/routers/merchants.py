# src/routers/merchants.py

from typing import List
from fastapi import APIRouter, Depends, status, Path, Query, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.merchant import MerchantCreate, MerchantUpdate, Merchant as MerchantSchema
from src.services.crud_merchant import MerchantService

router = APIRouter(
    prefix="/merchants",
    tags=["Merchants"]
)

# Create
@router.post(
    "/",
    response_model=MerchantSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new merchant"
)
def create_merchant(
    merchant: MerchantCreate,
    db: Session = Depends(get_db)
):
    try:
        return MerchantService.create_merchant(db, merchant)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Read All
@router.get(
    "/",
    response_model=List[MerchantSchema],
    summary="Retrieve all merchants"
)
def get_merchants(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    return MerchantService.get_merchants(db, skip=skip, limit=limit)


# Read By ID
@router.get(
    "/{merchant_id}",
    response_model=MerchantSchema,
    summary="Retrieve a merchant by ID"
)
def get_merchant_by_id(
    merchant_id: int = Path(..., gt=0, description="ID of the merchant to retrieve"),
    db: Session = Depends(get_db)
):
    merchant = MerchantService.get_merchant(db, merchant_id)
    if not merchant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Merchant not found")
    return merchant


# Update
@router.put(
    "/{merchant_id}",
    response_model=MerchantSchema,
    summary="Update a merchant by ID"
)
def update_merchant(
    merchant_id: int = Path(..., gt=0, description="ID of the merchant to update"),
    update_data: MerchantUpdate = ...,
    db: Session = Depends(get_db)
):
    merchant = MerchantService.get_merchant(db, merchant_id)
    if not merchant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Merchant not found")
    
    try:
        return MerchantService.update_merchant(db, merchant, update_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Delete
@router.delete(
    "/{merchant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a merchant by ID"
)
def delete_merchant(
    merchant_id: int = Path(..., gt=0, description="ID of the merchant to delete"),
    db: Session = Depends(get_db)
):
    merchant = MerchantService.get_merchant(db, merchant_id)
    if not merchant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Merchant not found")
    
    MerchantService.delete_merchant(db, merchant)
    return None
