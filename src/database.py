from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import settings

SQLALCHEMY_DATABASE_URL = (
    f"{settings.database_driver}://"
    f"{settings.database_username}:{settings.database_password}@"
    f"{settings.database_host}:{settings.database_port}/"
    f"{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
