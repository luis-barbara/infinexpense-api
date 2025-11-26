# tests/test_receipts.py

from fastapi import status
from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def test_merchant(client):
    """
    Fixture auxiliar: Cria um mercado de teste e retorna o ID.
    É necessário porque não se pode criar um recibo sem um merchant_id válido.
    """
    payload = {
        "name": "Test Merchant",
        "location": "Lisboa"}
    response = client.post("/merchants/", json=payload)
    
    if response.status_code == 409:
        payload["name"] = "Test Merchant 2"
        response = client.post("/merchants/", json=payload)
    
    assert response.status_code == 201, f"Failed to create merchant: {response.json()}"
    return response.json()["id"]


def test_create_receipt(client: TestClient, test_merchant):
    """POST /receipts - criar um recibo"""
    payload = {
        "merchant_id": test_merchant,
        "purchase_date": "2023-11-20",
        "barcode": "12345"
    }
    response = client.post("/receipts/", json=payload)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    
    # Verificações 
    assert data["merchant_id"] == test_merchant
    assert data["purchase_date"] == "2023-11-20"
    assert data["id"] is not None
    
    # Verificação crítica: recibo novo sem produtos deve ter total 0.00
    assert float(data["total_price"]) == 0.00


def test_list_receipts(client: TestClient, test_merchant):
    """GET /receipts - listar todos os recibos"""
    # Criar 2 recibos de teste
    client.post("/receipts/", json={
        "merchant_id": test_merchant,
        "purchase_date": "2023-11-20"
    })
    client.post("/receipts/", json={
        "merchant_id": test_merchant,
        "purchase_date": "2023-11-21"
    })
    
    response = client.get("/receipts/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verificações
    assert isinstance(data, list)
    assert len(data) == 2  
    assert "total_price" in data[0]


def test_get_receipt_by_id(client: TestClient, test_merchant):
    """GET /receipts/{id} - obter recibo pelo ID"""
    # Criar recibo
    create_resp = client.post("/receipts/", json={
        "merchant_id": test_merchant,
        "purchase_date": "2023-11-20"
    })
    receipt_id = create_resp.json()["id"]
    
    # Obter por ID
    response = client.get(f"/receipts/{receipt_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == receipt_id
    # Verifica se o objeto 'merchant' veio nested (com objeto la dentro)
    assert data["merchant"]["id"] == test_merchant


def test_update_receipt(client: TestClient, test_merchant):
    """PUT /receipts/{id} - atualizar recibo"""
    # Criar recibo
    create_resp = client.post("/receipts/", json={
        "merchant_id": test_merchant,
        "purchase_date": "2023-11-20"
    })
    receipt_id = create_resp.json()["id"]
    
    # Atualizar data
    response = client.put(
        f"/receipts/{receipt_id}",
        json={"purchase_date": "2023-12-01"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["purchase_date"] == "2023-12-01"
    # Verifica se o merchant_id não mudou
    assert data["merchant_id"] == test_merchant


def test_delete_receipt(client: TestClient, test_merchant):
    """DELETE /receipts/{id} - eliminar recibo"""
    # Criar recibo
    create_resp = client.post("/receipts/", json={
        "merchant_id": test_merchant,
        "purchase_date": "2023-11-20"
    })
    receipt_id = create_resp.json()["id"]
    
    # Eliminar
    response = client.delete(f"/receipts/{receipt_id}")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verificar que foi eliminado 
    get_resp = client.get(f"/receipts/{receipt_id}")
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND


def test_receipt_not_found(client: TestClient):
    """Teste de Erro: Tentar aceder a recibo inexistente"""
    response = client.get("/receipts/99999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Receipt not found"


def test_create_receipt_invalid_merchant(client: TestClient):
    """Teste de Erro: Criar recibo com merchant que não existe"""
    payload = {
        "merchant_id": 99999,  # ID inexistente
        "purchase_date": "2023-11-20"
    }
    response = client.post("/receipts/", json=payload)
    
    # O service lança ValueError -> Router retorna 400 Bad Request
    assert response.status_code == status.HTTP_400_BAD_REQUEST
