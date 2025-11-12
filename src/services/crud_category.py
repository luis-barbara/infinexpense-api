# src/services/crud_category.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from src.models import category as category_model
from src.schemas import category as category_schema


class CategoryService:
    # Read 
    def get_category(db: Session, category_id: int) -> Optional[category_model.Category]:
        """
        Obtem uma categoria através do ID
        """
        return db.query(category_model.Category).filter(
            category_model.Category.id == category_id).first()


    def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[category_model.Category]:
        """
        Obtem uma lista de categorias com paginação.
        """
        return (
        db.query(category_model.Category)
        .offset(skip)
        .limit(limit)
        .all()
        )


    # Create
    def create_category(db: Session, category_data: category_schema.CategoryCreate) -> category_model.Category:
        """
        Cria uma nova categoria.
        """
        # Verificar se existem duplicados
        existing = db.query(category_model.Category).filter_by(name=category_data.name).first()
        if existing:
            raise ValueError(f"Category '{category_data.name}' already exists.")

        db_category = category_model.Category(**category_data.model_dump())
        db.add(db_category)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

        db.refresh(db_category)
        return db_category



    # Update
    def update_category(db: Session, db_category: category_model.Category, update_data: category_schema.CategoryUpdate) -> category_model.Category:
        """
        Atualiza uma categoria existente.
        """
        update_dict = update_data.model_dump(exclude_unset=True)


        # Verificar se existe o nome duplicado
        if 'name' in update_dict:
            existing = db.query(category_model.Category).filter_by(name=update_dict['name']).first()
            if existing and existing.id != db_category.id:
                raise ValueError(f"Category '{update_dict['name']}' already exists.")

        for key, value in update_dict.items():
            setattr(db_category, key, value)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

        db.refresh(db_category)
        return db_category



    # Delete
    def delete_category(db: Session, db_category: category_model.Category) -> category_model.Category:
        """
        Apaga uma categoria.
        """
        db.delete(db_category)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

        return db_category