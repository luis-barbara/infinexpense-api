"""
Tests for ReceiptProductService - CRUD operations for receipt product items.
Tests the business logic for creating, reading, updating, and deleting products in receipts.
"""

import pytest
from decimal import Decimal
from src.services.crud_receipt_product import ReceiptProductService
from src.schemas.product import ProductCreate, ProductUpdate


@pytest.fixture
def test_product_for_receipt(client, test_category, test_unit):
    """Create a test product to use in receipts"""
    response = client.post("/products/", json={
        "name": "Test Receipt Product",
        "barcode": "999888777",
        "category_id": test_category,
        "measurement_unit_id": test_unit,
        "current_price": 10.00
    })
    assert response.status_code == 201
    return response.json()["id"]


@pytest.fixture
def test_merchant_for_receipt(client):
    """Create a test merchant for receipts"""
    response = client.post("/merchants/", json={
        "name": "Receipt Test Merchant",
        "location": "Test Location",
        "notes": "For testing"
    })
    assert response.status_code == 201
    return response.json()["id"]


@pytest.fixture
def test_receipt_for_products(client, test_merchant_for_receipt):
    """Create a test receipt for product items"""
    response = client.post("/receipts/", json={
        "merchant_id": test_merchant_for_receipt,
        "purchase_date": "2023-11-20"
    })
    assert response.status_code == 201
    return response.json()["id"]


class TestReceiptProductServiceCreate:
    """Tests for creating receipt product items"""

    def test_create_product_item_success(self, db, test_product_for_receipt, test_receipt_for_products):
        """Create a product item successfully"""
        product_data = ProductCreate(
            price=Decimal("5.99"),
            quantity=Decimal("2"),
            description="Test item",
            product_list_id=test_product_for_receipt
        )
        
        result = ReceiptProductService.create_product_item_for_receipt(
            db, 
            test_receipt_for_products, 
            product_data
        )
        
        assert result.id is not None
        assert result.price == Decimal("5.99")
        assert result.quantity == Decimal("2")
        assert result.description == "Test item"
        assert result.receipt_id == test_receipt_for_products
        assert result.product_list_id == test_product_for_receipt


class TestReceiptProductServiceRead:
    """Tests for reading receipt product items"""

    def test_get_product_item_by_id(self, db, test_product_for_receipt, test_receipt_for_products):
        """Get a product item by ID"""
        product_data = ProductCreate(
            price=Decimal("7.99"),
            quantity=Decimal("3"),
            product_list_id=test_product_for_receipt
        )
        
        created = ReceiptProductService.create_product_item_for_receipt(
            db, 
            test_receipt_for_products, 
            product_data
        )
        
        result = ReceiptProductService.get_product_item(db, created.id)
        
        assert result is not None
        assert result.id == created.id
        assert result.price == Decimal("7.99")
        assert result.quantity == Decimal("3")



class TestReceiptProductServiceUpdate:
    """Tests for updating receipt product items"""

    def test_update_product_item_price(self, db, test_product_for_receipt, test_receipt_for_products):
        """Update the price of a product item"""
        product_data = ProductCreate(
            price=Decimal("5.00"),
            quantity=Decimal("2"),
            product_list_id=test_product_for_receipt
        )
        
        item = ReceiptProductService.create_product_item_for_receipt(
            db, 
            test_receipt_for_products, 
            product_data
        )
        
        update_data = ProductUpdate(price=Decimal("6.50"))
        
        result = ReceiptProductService.update_product_item(db, item, update_data)
        
        assert result.price == Decimal("6.50")
        assert result.quantity == Decimal("2")



class TestReceiptProductServiceDelete:
    """Tests for deleting receipt product items"""

    def test_delete_product_item(self, db, test_product_for_receipt, test_receipt_for_products):
        """Delete a product item"""
        product_data = ProductCreate(
            price=Decimal("5.00"),
            quantity=Decimal("2"),
            product_list_id=test_product_for_receipt
        )
        
        item = ReceiptProductService.create_product_item_for_receipt(
            db, 
            test_receipt_for_products, 
            product_data
        )
        item_id = item.id
        
        result = ReceiptProductService.delete_product_item(db, item)
        
        assert result.id == item_id
