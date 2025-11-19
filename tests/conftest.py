import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.database import Base, get_db


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