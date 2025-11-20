# tests/test_products.py

from fastapi import status
from fastapi.testclient import TestClient


def test_create_product(client: TestClient):
    """POST /products - criar um produto na lista de produtos"""
    # criar produto
    payload = {
        "name": "Delta Cafe",
        "barcode": "1234567890123",
        "category_id": test_category,
        "measurement_unit_id": test_unit,
        "current_price": 9.99
    }
    response = client.post("/products/", json=payload)
    
    # verificação
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["category_id"] == payload["category_id"]
    assert "id" in data


def test_list_products(client: TestClient):
    """GET /products - listar produtos na lista de produtos"""

    # criar 2 produtos de teste
    client.post("/products/", json={
        "name": "Test Product 1",
        "barcode": "1234567890123",
        "category_id": test_category,
        "measurement_unit_id": test_unit,
        "current_price": 4.99
    })
    client.post("/products/", json={
        "name": "Test Product 2",
        "barcode": "9876543210987",
        "category_id": test_category,
        "measurement_unit_id": test_unit,
        "current_price": 19.99
    })
    
    response = client.get("/products/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2  
