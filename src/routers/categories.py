# src/routers/categories.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session
from datetime import date
import logging

from src.database import get_db
from src.schemas.category import CategoryCreate, CategoryUpdate, Category as CategorySchema
from src.services.crud_category import CategoryService


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post(
    "/", 
    response_model=CategorySchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category"
)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category."""
    try:
        return CategoryService.create_category(db, category)
    except ValueError as e:
        logger.warning(f"Validation error creating category: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error in create_category endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating category"
        )


@router.get(
    "/", 
    response_model=List[CategorySchema], 
    summary="Retrieve all categories"
)
def get_categories(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    start_date: date = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: date = Query(None, description="Filter by end date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    try:
        return CategoryService.get_categories(db, skip=skip, limit=limit, start_date=start_date, end_date=end_date)
    except Exception as e:
        logger.error(f"Error in get_categories endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching categories"
        )


@router.get(
    "/{category_id}", 
    response_model=CategorySchema,
    summary="Retrieve a category by its ID"
)
def get_category_by_id(category_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    try:
        category = CategoryService.get_category(db, category_id)
        if not category:
            logger.warning(f"Category not found: {category_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return category
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching category {category_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching category"
        )


@router.put(
    "/{category_id}", 
    response_model=CategorySchema,
    summary="Update an existing category by its ID"
)
def update_category(
    category_id: int = Path(..., gt=0),
    category_update: CategoryUpdate = ...,
    db: Session = Depends(get_db)
):
    try:
        db_category = CategoryService.get_category(db, category_id)
        if not db_category:
            logger.warning(f"Category not found for update: {category_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        
        return CategoryService.update_category(db, db_category, category_update)
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Validation error updating category {category_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating category {category_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating category"
        )


@router.delete(
    "/{category_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a category by its ID"
)
def delete_category(category_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    try:
        db_category = CategoryService.get_category(db, category_id)
        if not db_category:
            logger.warning(f"Category not found for deletion: {category_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        
        CategoryService.delete_category(db, db_category)
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting category {category_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting category"
        )
