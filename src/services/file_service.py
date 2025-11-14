import os
import shutil
import uuid
import logging
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models import product as model_product_list
from . import crud_product_list

# Configurações 
UPLOAD_DIRECTORY = Path("/app/uploads/products")
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Logging
logger = logging.getLogger(__name__)

# Tipos e extensões permitidas
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}

# Tamanho máximo do ficheiro (em bytes)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def save_product_photo(
    db: Session,
    product_list_id: int,
    file: UploadFile
) -> model_product_list.ProductList:
    """Faz upload de uma foto para a ProductList com validações reforçadas."""

    # 1. Validar produto
    db_product = crud_product_list.get_product_list(db, product_list_id)
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
    file_path_on_disk = UPLOAD_DIRECTORY / safe_filename
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
    if db_product.photo_url:
        try:
            old_file_path = os.path.join("/app", db_product.photo_url.lstrip('/'))
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        except Exception as e:
            logger.warning(f"Failed to delete old photo {db_product.photo_url}: {e}")

    # 7. Atualizar Base de Dados
    db_product.photo_url = file_path_in_db
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
