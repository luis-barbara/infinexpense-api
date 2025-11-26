from fastapi import status
from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def test_create_merchant(client: TestClient, test_category, test_unit):
    """POST /merchants - criar um comerciante na lista de comerciantes"""
    # criar comerciante
    payload = {
        "name": "Continente Bom Dia",
        "location": "Faro",
        "notes": "Supermercado local",
    }
    response = client.post("/merchants/", json=payload)
    
    # verificação
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == payload["name"]

def test_create_merchant_error(client: TestClient, test_category, test_unit):
    """POST /merchants - criar um comerciante com nome vazio deve falhar"""
 
    payload = {
        "name": None,
        "location": "Faro",
        "notes": "Supermercado local",
    }
    response = client.post("/merchants/", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_duplicated_merchant_error(client: TestClient, test_category, test_unit):
    """
    Error Test: Try to create two merchants with the same name.
    Should return 500 Internal Server Error due to database constraint violation.
    """
    payload = {
        "name": "Unique Merchant",
        "location": "Lisbon",
        "notes": "Some notes",
    }

    # First one succeeds
    response1 = client.post("/merchants/", json=payload)
    assert response1.status_code == status.HTTP_201_CREATED
    
    # Second one (same name) should fail with constraint violation
    response2 = client.post("/merchants/", json=payload)
    
    assert response2.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "detail" in response2.json()


# ==================== READ TESTS ====================

def test_get_all_merchants(client: TestClient, test_category, test_unit):
    """GET /merchants - Retrieve all merchants"""
    # Create multiple merchants
    merchants_data = [
        {"name": "Merchant 1", "location": "Lisbon", "notes": "Notes 1"},
        {"name": "Merchant 2", "location": "Porto", "notes": "Notes 2"},
        {"name": "Merchant 3", "location": "Faro", "notes": "Notes 3"},
    ]
    
    for merchant in merchants_data:
        client.post("/merchants/", json=merchant)
    
    # Get all merchants
    response = client.get("/merchants/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3
    assert data[0]["name"] == "Merchant 1"
    assert data[1]["name"] == "Merchant 2"
    assert data[2]["name"] == "Merchant 3"


def test_get_merchant_by_id(client: TestClient, test_category, test_unit):
    """GET /merchants/{id} - Retrieve a specific merchant by ID"""
    # Create a merchant
    payload = {"name": "Test Merchant", "location": "Lisbon", "notes": "Test notes"}
    create_response = client.post("/merchants/", json=payload)
    merchant_id = create_response.json()["id"]
    
    # Get merchant by ID
    response = client.get(f"/merchants/{merchant_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == merchant_id
    assert data["name"] == payload["name"]
    assert data["location"] == payload["location"]


def test_get_merchant_by_id_not_found(client: TestClient, test_category, test_unit):
    """GET /merchants/{id} - Should return 404 when merchant doesn't exist"""
    response = client.get("/merchants/9999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Merchant not found" in response.json()["detail"]


# ==================== UPDATE TESTS ====================

def test_update_merchant(client: TestClient, test_category, test_unit):
    """PUT /merchants/{id} - Update a merchant"""
    # Create a merchant
    create_payload = {"name": "Old Name", "location": "Lisbon", "notes": "Old notes"}
    create_response = client.post("/merchants/", json=create_payload)
    merchant_id = create_response.json()["id"]
    
    # Update the merchant
    update_payload = {
        "name": "New Name",
        "location": "Porto",
        "notes": "New notes"
    }
    response = client.put(f"/merchants/{merchant_id}", json=update_payload)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == merchant_id
    assert data["name"] == update_payload["name"]
    assert data["location"] == update_payload["location"]
    assert data["notes"] == update_payload["notes"]


def test_update_merchant_not_found(client: TestClient, test_category, test_unit):
    """PUT /merchants/{id} - Should return 404 when merchant doesn't exist"""
    update_payload = {"name": "New Name", "location": "Porto"}
    response = client.put("/merchants/9999", json=update_payload)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Merchant not found" in response.json()["detail"]


# ==================== DELETE TESTS ====================

def test_delete_merchant(client: TestClient, test_category, test_unit):
    """DELETE /merchants/{id} - Delete a merchant"""
    # Create a merchant
    create_payload = {"name": "To Delete", "location": "Lisbon", "notes": "Will be deleted"}
    create_response = client.post("/merchants/", json=create_payload)
    merchant_id = create_response.json()["id"]
    
    # Delete the merchant
    response = client.delete(f"/merchants/{merchant_id}")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify merchant is deleted
    get_response = client.get(f"/merchants/{merchant_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_merchant_not_found(client: TestClient, test_category, test_unit):
    """DELETE /merchants/{id} - Should return error when merchant doesn't exist"""
    response = client.delete("/merchants/9999")
    
    # Service catches exception and returns 400 BAD_REQUEST
    assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST]

