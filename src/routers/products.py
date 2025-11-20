# src/routers/products.py

from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query, Path, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.database import get_db
from src.schemas.product import (
    ProductListCreate,
    ProductListUpdate,
    ProductList as ProductListSchema
)
from src.services.crud_product_list import ProductListService 

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# Create
@router.post(
    "/",
    response_model=ProductListSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product"
)
def create_product(
    product: ProductListCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new product with the provided details.
    """
    try:
        return ProductListService.create_product_list(db, product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Product with name '{product.name}' already exists"
        )


# Read All
@router.get(
    "/",
    response_model=List[ProductListSchema],
    summary="Retrieve all products"
)
def get_all_products(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    barcode: Optional[str] = Query(None, description="Filter by product barcode"),
    measurement_unit_id: Optional[int] = Query(None, description="Filter by measurement unit ID"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all products with optional filters and pagination.
    """
    return ProductListService.get_product_lists(db, skip=skip, limit=limit)


# Read By ID
@router.get(
    "/{product_id}",
    response_model=ProductListSchema,
    summary="Retrieve a product by ID"
)
def get_product_by_id(
    product_id: int = Path(..., ge=1, description="ID of the product to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific product by its ID.
    """
    product = ProductListService.get_product_list(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


# Read By Barcode
@router.get(
    "/barcode/{barcode}",
    response_model=ProductListSchema,
    summary="Retrieve a product by barcode"
)
def get_product_by_barcode_endpoint(
    barcode: str = Path(..., max_length=50, description="Barcode of the product to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a product by its barcode.
    """
    product = ProductListService.get_product_by_barcode(db, barcode)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


# Read By Name
@router.get(
    "/name/{name}",
    response_model=ProductListSchema,
    summary="Retrieve a product by name"
)
def get_product_by_name_endpoint(
    name: str = Path(..., max_length=255, description="Name of the product to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a product by its name.
    """
    product = ProductListService.get_product_by_name(db, name)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


# Update
@router.put(
    "/{product_id}",
    response_model=ProductListSchema,
    summary="Update a product"
)
def update_product(
    product_id: int = Path(..., ge=1, description="ID of the product to update"),
    product_update: ProductListUpdate = None,
    db: Session = Depends(get_db)
):
    """
    Update a product's details.
    """
    product = ProductListService.update_product_list(db, product_id, product_update)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


# Delete
@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product"
)
def delete_product(
    product_id: int = Path(..., ge=1, description="ID of the product to delete"),
    db: Session = Depends(get_db)
):
    """
    Delete a product by its ID.
    """
    try:
        success = ProductListService.delete_product_list(db, product_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    except Exception as e:
        error_message = str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)
