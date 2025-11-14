# src/routers/categories.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.category import CategoryCreate, CategoryUpdate, Category as CategorySchema
from src.services.crud_category import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

# Create a new category
@router.post(
    "/", 
    response_model=CategorySchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category"
)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return CategoryService.create_category(db, category)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Get all categories with optional pagination
@router.get(
    "/", 
    response_model=List[CategorySchema], 
    summary="Retrieve all categories"
)
def get_categories(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    return CategoryService.get_categories(db, skip=skip, limit=limit)

# Get category by ID
@router.get(
    "/{category_id}", 
    response_model=CategorySchema,
    summary="Retrieve a category by its ID"
)
def get_category_by_id(category_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    category = CategoryService.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

# Update a category by ID
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
    db_category = CategoryService.get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    try:
        return CategoryService.update_category(db, db_category, category_update)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Delete a category by ID
@router.delete(
    "/{category_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a category by its ID"
)
def delete_category(category_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_category = CategoryService.get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    CategoryService.delete_category(db, db_category)
    return None
