import os
import shutil
import uuid
import logging
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models import product as model_product_list
from src.models import receipt as model_receipt
from .crud_product_list import ProductListService
from .crud_receipt import ReceiptService

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PRODUCT_UPLOAD_DIRECTORY = BASE_DIR / "uploads" / "products"
RECEIPT_UPLOAD_DIRECTORY = BASE_DIR / "uploads" / "receipts"

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}

MAX_FILE_SIZE = 5 * 1024 * 1024


def save_product_photo(
    db: Session,
    product_list_id: int,
    file: UploadFile
) -> model_product_list.ProductList:
    """Upload and save a photo for a product with validation."""
    db_product = ProductListService.get_product_list(db, product_list_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ProductList not found"
        )

    # 2. Validar tipo de ficheiro
    file_extension = Path(file.filename).suffix.lower()
    if not file.content_type or file.content_type not in ALLOWED_MIME_TYPES or file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # 3. Validar tamanho máximo
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum allowed size is {MAX_FILE_SIZE // (1024*1024)} MB"
        )

    # 4. Gerar nome seguro
    safe_filename = f"product_{product_list_id}_{uuid.uuid4()}{file_extension}"
    file_path_on_disk = PRODUCT_UPLOAD_DIRECTORY / safe_filename
    file_path_in_db = f"/uploads/products/{safe_filename}"

    # 5. Gravar no disco
    try:
        with open(file_path_on_disk, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file to disk: {e}"
        )
    finally:
        file.file.close()

    # 6. Apagar foto antiga
    if db_product.product_list_photo:
        try:
            old_file_path = BASE_DIR / db_product.photo_url.lstrip('/')
            
            ########## old_file_path = os.path.join("/app", db_product.product_list_photo.lstrip('/'))
            
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        except Exception as e:
            logger.warning(f"Failed to delete old photo {db_product.product_list_photo}: {e}")

    # 7. Atualizar Base de Dados
    db_product.product_list_photo = file_path_in_db
    db.add(db_product)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while updating photo URL"
        )

    db.refresh(db_product)
    return db_product




def save_receipt_photo(
    db: Session,
    receipt_id: int,
    file: UploadFile
) -> model_receipt.Receipt:
    """Faz upload de uma foto para o Receipt com validações reforçadas."""

    # 1. Validar receipt
    try:
        db_receipt = ReceiptService.get_receipt_by_id(db, receipt_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found"
        )

    # 2. Validar tipo de ficheiro
    file_extension = Path(file.filename).suffix.lower()
    if not file.content_type or file.content_type not in ALLOWED_MIME_TYPES or file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # 3. Validar tamanho máximo
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum allowed size is {MAX_FILE_SIZE // (1024*1024)} MB"
        )

    # 4. Gerar nome seguro
    safe_filename = f"receipt_{receipt_id}_{uuid.uuid4()}{file_extension}"
    file_path_on_disk = RECEIPT_UPLOAD_DIRECTORY / safe_filename
    file_path_in_db = f"/uploads/receipts/{safe_filename}"

    # 5. Gravar no disco
    try:
        with open(file_path_on_disk, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file to disk: {e}"
        )
    finally:
        file.file.close()

    # 6. Apagar foto antiga
    if db_receipt.receipt_photo:
        try:
            old_file_path = os.path.join("/app", db_receipt.receipt_photo.lstrip('/'))
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        except Exception as e:
            logger.warning(f"Failed to delete old receipt photo {db_receipt.receipt_photo}: {e}")

    # 7. Atualizar Base de Dados
    db_receipt.receipt_photo = file_path_in_db
    db.add(db_receipt)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while updating receipt photo URL"
        )

    db.refresh(db_receipt)
    return db_receipt