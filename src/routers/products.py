# src/routers/products.py

from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query, Path, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.product import (
    ProductListCreate,
    ProductListUpdate,
    ProductList as ProductListSchema
)
from src.services.crud_product_list import (
    create_product_list,
    get_product_list as get_product_list_by_id,
    get_product_lists,
    get_product_by_barcode,
    get_product_by_name
)

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
    return create_product_list(db, product)


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
    return get_product_lists(
        db=db,
        skip=skip,
        limit=limit,
        barcode=barcode,
        measurement_unit_id=measurement_unit_id,
        category_id=category_id
    )


# Read By 
@router.get(
    "/{product_id}",
    response_model=ProductListSchema,
    summary="Retrieve a product by ID"
)
def get_product_by_id(
    product_id: int = Path(..., ge=1, description="ID of the product to retrieve"),
    db: Session = Depends(get_db)
):
    product = get_product_list_by_id(db, product_id)
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
    product = get_product_by_barcode(db, barcode)
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
    product = get_product_by_name(db, name)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
