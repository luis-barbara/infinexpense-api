# src/routers/merchants.py

from typing import List
from fastapi import APIRouter, Depends, status, Path, Query, HTTPException
from sqlalchemy.orm import Session
import logging

from src.database import get_db
from src.schemas.merchant import MerchantCreate, MerchantUpdate, Merchant as MerchantSchema
from src.services.crud_merchant import MerchantService


logger = logging.getLogger(__name__)


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
    """
    Create a new merchant.
    """
    try:
        return MerchantService.create_merchant(db, merchant)
    except Exception as e:
        logger.error(f"Error in create_merchant endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


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
    try:
        return MerchantService.get_merchants(db, skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Error in get_merchants endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching merchants"
        )


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
    try:
        merchant = MerchantService.get_merchant(db, merchant_id)
        if not merchant:
            logger.warning(f"Merchant not found: {merchant_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Merchant not found")
        return merchant
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching merchant {merchant_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching merchant"
        )


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
    try:
        merchant = MerchantService.get_merchant(db, merchant_id)
        if not merchant:
            logger.warning(f"Merchant not found for update: {merchant_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Merchant not found")
        
        return MerchantService.update_merchant(db, merchant, update_data)
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Validation error updating merchant {merchant_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating merchant {merchant_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating merchant"
        )


# Delete
@router.delete(
    "/{merchant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a merchant"
)
def delete_merchant(
    merchant_id: int = Path(..., ge=1, description="ID of the merchant to delete"),
    db: Session = Depends(get_db)
):
    """
    Delete a merchant by its ID.
    """
    try:
        success = MerchantService.delete_merchant(db, merchant_id)
        if not success:
            logger.warning(f"Merchant not found for deletion: {merchant_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Merchant not found")
    except HTTPException:
        raise
    except Exception as e:
        error_message = str(e)
        logger.error(f"Error deleting merchant {merchant_id}: {error_message}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)