from fastapi import status
from fastapi.testclient import TestClient
import pytest


# ==================== CREATE TESTS ====================

def test_create_category(client: TestClient):
    """POST /categories - Create a new category"""
    payload = {"name": "Groceries"}
    response = client.post("/categories/", json=payload)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == payload["name"]
    assert "id" in data



def test_create_category_error_empty_name(client: TestClient):
    """POST /categories - Creating a category with empty name should fail"""
    payload = {"name": ""}
    response = client.post("/categories/", json=payload)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT



def test_create_duplicated_category_error(client: TestClient):
    """POST /categories - Creating two categories with the same name should fail"""
    payload = {"name": "Unique Category"}
    
    # First one succeeds
    response1 = client.post("/categories/", json=payload)
    assert response1.status_code == status.HTTP_201_CREATED
    
    # Second one (same name) should fail with 400 or 500
    response2 = client.post("/categories/", json=payload)
    assert response2.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_500_INTERNAL_SERVER_ERROR]


# ==================== READ TESTS ====================

def test_get_all_categories(client: TestClient):
    """GET /categories - Retrieve all categories"""
    # Create multiple categories
    categories_data = ["Groceries", "Electronics", "Clothing", "Health"]
    
    for cat_name in categories_data:
        client.post("/categories/", json={"name": cat_name})
    
    # Get all categories
    response = client.get("/categories/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 4
    names = [cat["name"] for cat in data]
    assert "Groceries" in names
    assert "Electronics" in names


def test_get_category_by_id(client: TestClient):
    """GET /categories/{id} - Retrieve a specific category by ID"""
    # Create a category
    create_payload = {"name": "Test Category"}
    create_response = client.post("/categories/", json=create_payload)
    category_id = create_response.json()["id"]
    
    # Get category by ID
    response = client.get(f"/categories/{category_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == category_id
    assert data["name"] == create_payload["name"]


def test_get_category_by_id_not_found(client: TestClient):
    """GET /categories/{id} - Should return 404 when category doesn't exist"""
    response = client.get("/categories/9999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Category not found" in response.json()["detail"]


# ==================== UPDATE TESTS ====================

def test_update_category(client: TestClient):
    """PUT /categories/{id} - Update a category"""
    # Create a category
    create_payload = {"name": "Old Name"}
    create_response = client.post("/categories/", json=create_payload)
    category_id = create_response.json()["id"]
    
    # Update the category
    update_payload = {"name": "New Name"}
    response = client.put(f"/categories/{category_id}", json=update_payload)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == category_id
    assert data["name"] == update_payload["name"]


def test_update_category_with_empty_name(client: TestClient):
    """PUT /categories/{id} - Updating with empty name should fail"""
    # Create a category
    create_response = client.post("/categories/", json={"name": "Test"})
    category_id = create_response.json()["id"]
    
    # Try to update with empty name
    update_payload = {"name": ""}
    response = client.put(f"/categories/{category_id}", json=update_payload)
    
    # Should either fail or reject the update
    assert response.status_code in [status.HTTP_422_UNPROCESSABLE_CONTENT, status.HTTP_400_BAD_REQUEST]


# ==================== DELETE TESTS ====================

def test_delete_category(client: TestClient):
    """DELETE /categories/{id} - Delete a category"""
    # Create a category
    create_response = client.post("/categories/", json={"name": "To Delete"})
    category_id = create_response.json()["id"]
    
    # Delete the category
    response = client.delete(f"/categories/{category_id}")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify category is deleted
    get_response = client.get(f"/categories/{category_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_category_not_found(client: TestClient):
    """DELETE /categories/{id} - Should return 404 when category doesn't exist"""
    response = client.delete("/categories/9999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Category not found" in response.json()["detail"]