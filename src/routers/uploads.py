# src/routers/uploads.py

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
import logging 

from src.database import get_db
from src.services import file_services
from src.schemas import product as schema_product
from src.schemas import receipt as schema_receipt

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"]
)


@router.post(
    "/product-list/{product_list_id}/photo",
    response_model=schema_product.ProductList,
    status_code=status.HTTP_200_OK 
)
def upload_product_list_photo(
    product_list_id: int,
    file: UploadFile = File(..., description="Image file (JPG, PNG)."),
    db: Session = Depends(get_db)
):
    """Upload a photo for a product in the master list."""
    try:
        updated_product = file_services.save_product_photo(
            db=db,
            product_list_id=product_list_id,
            file=file
        )

        return updated_product
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error uploading photo for product_list_id {product_list_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred on the server."
        )


@router.post(
    "/receipt/{receipt_id}/photo",
    response_model=schema_receipt.Receipt,
    status_code=status.HTTP_200_OK
)
def upload_receipt_photo(
    receipt_id: int,
    file: UploadFile = File(..., description="Image file (JPG, PNG)."),
    db: Session = Depends(get_db)
):
    """Upload a photo for a receipt."""
    try:
        updated_receipt = file_services.save_receipt_photo(
            db=db,
            receipt_id=receipt_id,
            file=file
        )

        return updated_receipt
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error uploading photo for receipt_id {receipt_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred on the server."
        )