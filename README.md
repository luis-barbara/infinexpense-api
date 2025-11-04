

# Estrutura do Projeto

/infinexpense-api/          # Pasta raiz do repositório 
|
|-- frontend/               # <--- PROJETO FRONTEND (Equipa Frontend)
|   |-- index.html
|   |-- css/
|   |-- js/
|
|-- src/                    # <--- PROJETO BACKEND (Equipa Backend)
|   |-- __init__.py
|   |-- main.py             # Ponto de entrada. Cria a app FastAPI e inclui routers.
|   |-- database.py         # Setup da sessão (Engine, Base, get_db).
|   |-- settings.py         
|   |
|   |-- models/
|   |   |-- __init__.py
|   |   |-- models.py       # Modelos SQLAlchemy (mapeia o diagrama DB).
|   |
|   |-- schemas/
|   |   |-- __init__.py
|   |   |-- receipt.py      # Modelos Pydantic para Recibos (Create, Read, Update).
|   |   |-- product.py      # Modelos Pydantic para Produtos.
|   |   |-- merchant.py     # ...
|   |   |-- report.py
|   |
|   |-- services/
|   |   |-- __init__.py
|   |   |-- crud_receipt.py     # Lógica de negócio (CRUD) para Recibos.
|   |   |-- crud_product.py     # Lógica de negócio (CRUD) para Produtos.
|   |   |-- ...
|   |   |-- reports_service.py     # Lógica de negócio (Queries complexas) para Relatórios.
|   |
|   |-- routers/
|   |   |-- __init__.py
|   |   |-- receipts.py     # Endpoints API para /receipts
|   |   |-- products.py     # Endpoints API para /products
|   |   |-- merchants.py    # ... 
|   |   |-- categories.py
|   |   |-- reports.py
|
|-- ops/                    # Pasta de Operações/Infraestrutura (Docker)
|   |-- ...
|
|-- alembic/                # Pasta do Alembic (Base de Dados)
|   |-- ... (ficheiros do alembic)
|   |-- 
|   |-- 
|
|-- tests/                  # Pasta para os testes unitários/integração
|   |-- ...
|
|-- pyproject.toml          # Ficheiro de configuração do Poetry 
|-- README.md