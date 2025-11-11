# src/services/crud_category.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from src.models import category as category_model
from src.schemas import category as category_schema


# Read
def get_category(db: Session, category_id: int) -> Optional[category_model.Category]:
    """
    Obtem uma categoria através do ID
    """
    return db.query(category_model.Category).filter(category_model.Category.id == category_id).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[model_category.Category]:
    """
    Obtém uma lista de categorias com paginação.
    """
    return (
    db.query(model_category.Category)
    .offset(skip)
    .limit(limit)
    .all()
    )