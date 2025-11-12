from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, status, Query, Path, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.product import (
    ProductListCreate,
    ProductListUpdate,
    ProductList as ProductListSchema
)
from src.services.crud_product_list import ProductListService as get_product_list

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)



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
    - **name**: Name of the product
    - **barcode**: Optional barcode of the product
    - **measurement_unit_id**: ID of the measurement unit
    - **category_id**: ID of the category
    Returns the created product.
    """
    return get_product_list.create_product(db, product)



@router.get(
    "/",
    response_model = List[ProductListSchema],
    summary="Retrieve all products",
)
def get_all_products(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    barcode: Optional[str] = Query(None, description="Filter by product barcode"),
    measurement_unit_id: Optional[int] = Query(None, description="Filter by measurement unit ID"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    db: Session = Depends(get_db),
):
    """
    Retrieve all products with pagination support.
    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of records to return
    - **barcode**: Optional filter by product barcode
    - **measurement_unit_id**: Optional filter by measurement unit ID
    - **category_id**: Optional filter by category ID
    Returns a list of products.
    """
    return get_product_list.get_all_products(
        db=db, 
        skip=skip, 
        limit=limit,
        barcode=barcode,
        measurement_unit_id=measurement_unit_id,
        category_id=category_id
)



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
    Retrieve a product by its ID.
    - **product_id**: ID of the product to retrieve
    Returns the product details.
    """
    product = get_product_list.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product



@router.get(
    "/barcode/{barcode}",
    response_model=ProductListSchema,
    summary="Retrieve a product by barcode"
)
def get_product_by_barcode(
    barcode: str = Path(..., max_length=50, description="Barcode of the product to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a product by its barcode.
    - **barcode**: Barcode of the product to retrieve
    Returns the product details.
    """
    product = get_product_list.get_product_by_barcode(db, barcode)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.get(
    "/name/{name}",
    response_model=ProductListSchema,
    summary="Retrieve a product by name"
)
def get_product_by_name(
    name: str = Path(..., max_length=255, description="Name of the product to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a product by its name.

    - **name**: The name associated with the product

    Returns the product details.
    """
    product = get_product_list.get_product_by_name(db, name)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    return product



