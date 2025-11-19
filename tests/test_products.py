# tests/test_products.py


from fastapi import status
from fastapi.testclient import TestClient



def create_dependencies(client: TestClient):
    # criar uma categoria de teste
    cat_payload = {"name": "Categoria Teste"}
    cat_response = client.post("/categories/", json=cat_payload)
    
    if cat_response.status_code == 201:
        cat_id = cat_response.json()["id"]
    else:
        cat_id = 1

    # criar uma unidade de medida de teste
    unit_payload = {"name": "Unidade Teste", "abbreviation": "UT"}
    unit_response = client.post("/measurement_units/", json=unit_payload)

    if unit_response.status_code == 201:
        unit_id = unit_response.json()["id"]
    else:
        unit_id = 1
    
    return cat_id, unit_id



def test_create_product(client: TestClient):
    """POST /products - criar um produto na lista de produtos"""
    cat_id, unit_id = create_dependencies(client)

    # criar produto
    payload = {
        "name": "Delta Cafe",
        "barcode": "1234567890123",
        "category_id": cat_id,
        "measurement_unit_id": unit_id,
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
    cat_id, unit_id = create_dependencies(client)

    # criar 2 produtos de teste
    client.post("/products/", json={
        "name": "Produto Teste 1",
        "barcode": "1234567890123",
        "category_id": cat_id,
        "measurement_unit_id": unit_id,
        "current_price": 4.99
    })

    client.post("/products/", json={
        "name": "Produto Teste 2",
        "barcode": "9876543210987",
        "category_id": cat_id,
        "measurement_unit_id": unit_id,
        "current_price": 19.99
    })

    response = client.get("/products/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert len(data) >= 2