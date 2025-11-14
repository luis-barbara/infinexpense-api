# src/routers/uploads.py

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
import logging 

# Importa as dependências (DB, Service, Schema de resposta)
from src.db.dependencies import get_db
from src.services import file_service 
from src.schemas import product as schema_product 


router = APIRouter(
    prefix="/uploads", 
    tags=["Uploads"]   
)


# Endpoint: Upload de Foto para a Lista de Produtos
@router.post(
    "/product-list/{product_list_id}/photo",
    response_model=schema_product.ProductList,
    status_code=status.HTTP_200_OK 
)
def upload_product_list_photo(
    product_list_id: int,
    file: UploadFile = File(..., description="O ficheiro de imagem (JPG, PNG) para o upload."),
    db: Session = Depends(get_db)
):
    """
    Faz o upload de uma foto para um item da lista-mestra de produtos.
    Isto tem de ser chamado como 'multipart/form-data'.
    
    Substitui a foto antiga, se existir.
    """
    

    try:
        updated_product = file_service.save_product_photo(
            db=db,
            product_list_id=product_list_id,
            file=file
        )

        return updated_product
    
    # Este 'except' é um "safeguard" (rede de segurança) para erros
    # *inesperados* que o 'file_service' não tenha previsto.
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Erro inesperado no upload de foto para product_list_id {product_list_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro inesperado no servidor."
        )
