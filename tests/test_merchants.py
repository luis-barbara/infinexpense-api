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

