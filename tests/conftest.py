# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.database import Base, get_db

"""
Configuração de Testes com TestClient e SQLite em Memória

Como funcionam os testes com pytest (sem servidor real):
- Fluxo normal: Utilizador -> Internet (Porta 8000) -> Uvicorn -> FastAPI
- Fluxo de teste: Pytest -> TestClient -> FastAPI (tudo em memória)

O TestClient simula requisições HTTP, fazendos chamadas às funções Python diretamente.
O SQLite :memory: substitui o PostgreSQL para testes rápidos e isolados.
Sem rede, sem Docker, sem portas - tudo corre num único processo Python.
"""


SQLALCHEMY_DATABASE_URL = ("sqlite:///:memory:")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esta fixture corre antes de CADA teste individual (scope="function")
@pytest.fixture(scope="function")
def db():
    """Cria uma nova base de dados em memória para cada teste."""
    # Cria todas as tabelas (Category, Product, Receipt, etc.)
    Base.metadata.create_all(bind=engine) # Cria as tabelas
    db = TestingSessionLocal() # Cria sessão
    try:
        yield db
    finally:
        db.close() # fecha sessao depois do teste
        Base.metadata.drop_all(bind=engine) # e apaga as tabelas

# Esta fixture cria o "navegador falso" que vai chamar a API
@pytest.fixture(scope="function")
def client(db):
    """Cria cliente HTTP para testar a API"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db # O FastAPI em vez de usar a configuração do settings.py (que procuraria o Postgres no Docker), ele usa esta conexão SQLite temporária
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear() 

# Como quase todos os testes precisam de categoria e unidade de medida,
# foram criadas estas fixtures para não repetir código
@pytest.fixture
def test_category(client):
    """cria uma categoria de teste"""
    response = client.post("/categories/", json={"name": "Test Category"})
    assert response.status_code == 201, f"Failed to create category: {response.json()}"
    return response.json()["id"]


@pytest.fixture
def test_unit(client):
    """cria uma unidade de medida de teste"""
    response = client.post("/measurement-units/", json={
        "name": "Test Unit",
        "abbreviation": "TU"
    })
    assert response.status_code == 201, f"Failed to create unit: {response.json()}"
    return response.json()["id"]
