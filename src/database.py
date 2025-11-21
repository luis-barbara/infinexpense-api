from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import settings

# Construct the database URL (URL de ligação à base de dados)
SQLALCHEMY_DATABASE_URL = (
    f"{settings.database_driver}://"
    f"{settings.database_username}:{settings.database_password}@"
    f"{settings.database_host}:{settings.database_port}/"
    f"{settings.database_name}"
)

# Create the SQLAlchemy engine (Gestor de ligações da applicação à base de dados)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal class for creating DB sessions (SQLAlchemy: criação de varias sessoes para as diferentes chamadas a API)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models (Class Base permite que todos os modelos criados em models.py 
# herdam desta class, para que o Alembic consiga encontrar os models, compara-los com a base de dados e criar as migrations)
Base = declarative_base()


# Dependency for getting DB session
# Abre uma nova sessão de DB (db = SessionLocal())
# 'yield db' -> Entrega a sessão ao endpoint
# 'finally: db.close()' -> Fecha a sessão após o endpoint terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
