# src/services/crud_product_list.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from src.models import product as product_list_model
from src.schemas import product as product_list_schema

from . import crud_measurement_unit
from . import crud_category


# Read
def get_product_list(db: Session, product_list_id: int) -> Optional[product_list_model.ProductList]:
    """
    Obtém um item da lista de produtos pelo ID
    """
    return db.query(product_list_model.ProductList).filter(
        product_list_model.ProductList.id == product_list_id).first()


def get_product_lists(db: Session, skip: int = 0, limit: int = 100) -> List[product_list_model.ProductList]:
    """
    Obtém a lista de produtos, com paginação.
    """
    return (
        db.query(product_list_model.ProductList)
        .offset(skip)
        .limit(limit)
        .all()
    )


# Create
def create_product_list(db: Session, product_list_data: product_list_schema.ProductListCreate) -> product_list_model.ProductList:
    """
    Cria um novo produto na lista de produtos.
    Verifica se as dependências (Categoria e Unidade) existem.
    """
    # Verificações
    # 1. O nome já existe? 
    existing = db.query(product_list_model.ProductList).filter_by(
        name=product_list_data.name).first()
    if existing:
        raise ValueError(f"ProductList name '{product_list_data.name}' already exists")

    # 2. A Categoria existe?
    category = crud_category.get_category(db, product_list_data.category_id)
    if not category:
        raise ValueError(f"Category ID '{product_list_data.category_id}' not found")

    # 3. A Unidade de Medida existe?
    unit = crud_measurement_unit.get_measurement_unit(db, product_list_data.measurement_unit_id)
    if not unit:
        raise ValueError(f"MeasurementUnit ID '{product_list_data.measurement_unit_id}' not found")
    

    # Se todas as verificações passarem, é criado o objeto
    db_product_list = product_list_model.ProductList(**product_list_data.model_dump())
    db.add(db_product_list)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Database constraint violation (e.g., duplicate barcode)")

    db.refresh(db_product_list)
    return db_product_list


# Update
def update_product_list(db: Session, db_product_list: product_list_model.ProductList,
                        update_data: product_list_schema.ProductListUpdate,
                        ) -> product_list_model.ProductList:
    """
    Atualiza um produto da lista-mestra.
    """
    update_dict = update_data.model_dump(exclude_unset=True)

    # Validação
    # 1. O nome está a ser mudado? Verifica se ja existe.
    if 'name' in update_dict:
        existing = db.query(product_list_model.ProductList).filter_by(
            name=update_dict['name']
        ).first()
        if existing and existing.id != db_product_list.id:
            raise ValueError(f"ProductList name '{update_dict['name']}' already exists")

    # 2. A Categoria está a ser mudada? Verifica se existe.
    if 'category_id' in update_dict:
        category = crud_category.get_category(db, update_dict['category_id'])
        if not category:
            raise ValueError(f"Category ID '{update_dict['category_id']}' not found")

    # 3. A Unidade de Medida está a ser mudada? Verifica se existe.
    if 'measurement_unit_id' in update_dict:
        unit = crud_measurement_unit.get_measurement_unit(db, update_dict['measurement_unit_id'])
        if not unit:
            raise ValueError(f"MeasurementUnit ID '{update_dict['measurement_unit_id']}' not found")
    

    # Se passar as validações, são aplicados os updates
    for key, value in update_dict.items():
        setattr(db_product_list, key, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Database constraint violation (e.g., duplicate barcode)")

    db.refresh(db_product_list)
    return db_product_list



# Delete
def delete_product_list(
    db: Session, db_product_list: product_list_model.ProductList) -> product_list_model.ProductList:
    """
    Apaga um produto da lista
    """
    db.delete(db_product_list)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # Caso algum produto (Item do Recibo) ainda estiver a apontar para este 'ProductList'
        raise ValueError("Cannot delete: this product definition is linked to existing receipts")
        
    return db_product_list
