# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.database import Base, get_db

# TestClient e SQLite
# Quando corremos o pytest no terminal, não existe nenhum servidor web real (Uvicorn) a correr, 
# não existem portas abertas (como a 8000), e não existe Docker. 
# Tudo acontece dentro de um único processo Python na memória do pc
# Normalmente, o fluxo é: Utilizador -> Internet (Porta 8000) -> Uvicorn (Servidor) -> FastAPI
# Nos testes com TestClient, o fluxo é: Pytest -> TestClient -> FastAPI
# O TestClient é um simulador: nao é enviada uma requisição HTTP pela rede,
# É criado um objeto que simula esse pedido e chama diretamente a função Python da API
# Depois é enviado o resultado como objeto que parece a reposta HTTP
# o "cliente" e o "servidor" são o mesmo programa a comunicar na memória RAM

# Sem Rede HTTP: O TestClient simula os pedidos HTTP chamando as funções Python diretamente.
# Sem Postgres: O conftest.py substitui o Postgres "pesado" por um SQLite em memória leve e instantâneo.

# "sqlite:///:memory:" significa que a DB vive na RAM, não no disco
SQLALCHEMY_DATABASE_URL = ("sqlite:///:memory:")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """Cria uma nova base de dados em memória para cada teste."""
    Base.metadata.create_all(bind=engine) # Cria as tabelas
    db = TestingSessionLocal() # Cria sessão
    try:
        yield db
    finally:
        db.close() # fecha sessao depois do teste
        Base.metadata.drop_all(bind=engine) # e apaga as tabelas


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
