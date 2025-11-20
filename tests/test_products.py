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


def test_get_product_by_id(client: TestClient, test_category, test_unit):
    """GET /products/{id} - get produto pelo ID"""
    # Create
    create_resp = client.post("/products/", json={
        "name": "Milk",
        "barcode": "3333",
        "category_id": test_category,
        "measurement_unit_id": test_unit
    })
    product_id = create_resp.json()["id"]
    
    # Get by ID
    response = client.get(f"/products/{product_id}")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Milk"


def test_update_product(client: TestClient, test_category, test_unit):
    """PUT /products/{id} - update product"""
    # Create
    create_resp = client.post("/products/", json={
        "name": "Cake",
        "barcode": "4444",
        "category_id": test_category,
        "measurement_unit_id": test_unit
    })
    product_id = create_resp.json()["id"]
    
    # Update (Para este caso: update name)
    response = client.put(
        f"/products/{product_id}",
        json={"name": "Chocolate Cake"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Chocolate Cake"
    assert data["barcode"] == "4444"


def test_delete_product(client: TestClient, test_category, test_unit):
    """DELETE /products/{id} - delete product"""
    # Create
    create_resp = client.post("/products/", json={
        "name": "Temporary",
        "barcode": "9999",
        "category_id": test_category,
        "measurement_unit_id": test_unit
    })
    product_id = create_resp.json()["id"]
    
    # Delete
    response = client.delete(f"/products/{product_id}")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    get_resp = client.get(f"/products/{product_id}")
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND


def test_create_duplicate_name_fails(client: TestClient, test_category, test_unit):
    """
    Error Test: Try to create two products with the same name.
    Should return 409 Conflict.
    """
    payload = {
        "name": "Unique Product",
        "category_id": test_category,
        "measurement_unit_id": test_unit
    }

    # First one succeeds
    client.post("/products/", json=payload)
    
    # Second one (same name) should fail
    response = client.post("/products/", json=payload)
    
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in response.json()["detail"]
