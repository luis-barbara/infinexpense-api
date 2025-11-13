# src/services/reports_service.py

from sqlalchemy.orm import Session
from sqlalchemy import func, case, distinct
from decimal import Decimal
from typing import List, Optional
from datetime import date

# Importa todos os 'models' e 'schemas' que vamos usar
from src.models import (
    merchant as model_merchant,
    receipt as model_receipt,
    product as model_product_list,
    receipt_product as model_receipt_product,
    category as model_category
)
from src.schemas import report as schema_report

# ---
# Relatório 1: GASTOS POR CATEGORIA (para o Gráfico do Dashboard)
# (Corresponde ao schema 'ReportSpendingByEntity' e ao 'imagem.png-10a83757...')
# ---
def get_spending_by_category(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[schema_report.ReportSpendingByEntity]:
    """
    Calcula o total gasto por categoria para o gráfico do dashboard,
    com filtro de data opcional.
    
    Esta query tem de:
    1. Juntar (JOIN) Categoria -> ProductList -> Product (Item do Recibo) -> Receipt
    2. Filtrar (FILTER) por data (no 'Receipt')
    3. Calcular o 'total_item' (price * quantity)
    4. Agrupar (GROUP BY) por category.id e category.name
    5. Somar (SUM) o 'total_item'
    """
    
    # 1. Define o cálculo do preço total por item
    total_item_spend = (model_receipt_product.Product.price * model_receipt_product.Product.quantity).label("total_item_spend")

    # 2. Inicia a query (o que queremos selecionar)
    query = db.query(
        model_category.Category.id.label("entity_id"),
        model_category.Category.name.label("name"),
        # Usamos func.coalesce para garantir que o SUM devolve 0 em vez de NULL
        func.coalesce(func.sum(total_item_spend), Decimal("0.00")).label("total_spent")
    )
    
    # 3. Define os JOINs (como as tabelas se ligam)
    # (Usamos 'isouter=True' (LEFT JOIN) para incluir categorias
    # que possam ter 0 gastos, se assim for desejado)
    
    # Categoria -> ProductList
    query = query.join(
        model_product_list.ProductList,
        model_category.Category.id == model_product_list.ProductList.category_id,
        isouter=True
    )
    # ProductList -> Product (Item do Recibo)
    query = query.join(
        model_receipt_product.Product,
        model_product_list.ProductList.id == model_receipt_product.Product.product_list_id,
        isouter=True
    )
    
    # 4. Filtros (Onde a lógica de data entra)
    
    # NOTA: O filtro de data tem de ser feito num 'join' ou 'subquery'
    # para não quebrar o LEFT JOIN (não excluir categorias com 0 recibos).
    # Vamos fazer um JOIN à tabela de Recibos...
    query = query.join(
        model_receipt.Receipt,
        model_receipt_product.Product.receipt_id == model_receipt.Receipt.id,
        isouter=True
    )
    
    # ...e aplicamos os filtros de data AQUI.
    if start_date:
        query = query.filter(model_receipt.Receipt.date >= start_date)
    if end_date:
        query = query.filter(model_receipt.Receipt.date <= end_date)

    # 5. Agrupamento (Grouping)
    query = query.group_by(model_category.Category.id, model_category.Category.name)
    
    # 6. Ordenação (Ordering)
    query = query.order_by(func.sum(total_item_spend).desc().nullslast())
    
    # 7. Executa a query
    results = query.all()
    
    # O Pydantic (graças ao 'from_attributes=True' e aos '.label()')
    # vai converter esta lista de 'Row objects' para o teu schema.
    return results

# ---
# Relatório 2: LISTA DE SUPERMERCADOS ENRIQUECIDA (para o Ecrã 4)
# (Corresponde ao schema 'MerchantReportData' e ao 'image_b893b5.png')
# ---
def get_enriched_merchant_report(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[schema_report.MerchantReportData]:
    """
    Calcula o relatório de supermercados (Ecrã 4).
    Isto tem de usar LEFT JOINs para incluir supermercados com 0 recibos.
    
    Esta query tem de:
    1. Começar no Merchant (Supermercado)
    2. Fazer LEFT JOIN para Recibos (Receipts)
    3. Fazer LEFT JOIN para Itens (Products)
    4. Aplicar os filtros de data de forma segura (numa subquery)
    5. Agrupar (GROUP BY) por merchant.id
    6. Calcular o COUNT(receipts) e o SUM(price * quantity)
    """

    # --- PASSO 1: Criar uma SubQuery (uma "tabela virtual")
    #    para os Recibos JÁ FILTRADOS por data.
    #    Isto é crucial para o LEFT JOIN funcionar.
    
    filtered_receipts_subq = db.query(
        model_receipt.Receipt.id,
        model_receipt.Receipt.merchant_id
    ).filter(model_receipt.Receipt.id != None) # Garante que a query é válida

    if start_date:
        filtered_receipts_subq = filtered_receipts_subq.filter(
            model_receipt.Receipt.date >= start_date
        )
    if end_date:
        filtered_receipts_subq = filtered_receipts_subq.filter(
            model_receipt.Receipt.date <= end_date
        )
    
    # Transforma a query numa "tabela" que podemos usar num JOIN
    filtered_receipts_subq = filtered_receipts_subq.subquery()

    # --- PASSO 2: Definir os nossos cálculos
    
    # Total Gasto (SUM)
    total_spent = func.coalesce(
        func.sum(model_receipt_product.Product.price * model_receipt_product.Product.quantity),
        Decimal("0.00")
    ).label("total_spent")
    
    # Contagem de Recibos (COUNT)
    receipt_count = func.count(
        func.distinct(filtered_receipts_subq.c.id)
    ).label("receipt_count")

    # --- PASSO 3: Query Principal (a partir do Merchant)
    
    query = db.query(
        model_merchant.Merchant.id,
        model_merchant.Merchant.name,
        model_merchant.Merchant.location,
        total_spent,
        receipt_count
    )
    
    # --- PASSO 4: Os LEFT JOINs
    
    # LEFT JOIN 1: Merchant -> Recibos (Já filtrados pela subquery)
    query = query.outerjoin(
        filtered_receipts_subq,
        model_merchant.Merchant.id == filtered_receipts_subq.c.merchant_id
    )
    
    # LEFT JOIN 2: Recibos (Filtrados) -> Itens do Recibo
    query = query.outerjoin(
        model_receipt_product.Product,
        filtered_receipts_subq.c.id == model_receipt_product.Product.receipt_id
    )
    
    # --- PASSO 5: Agrupamento (GROUP BY)
    # Agrupa pelo Supermercado
    query = query.group_by(
        model_merchant.Merchant.id,
        model_merchant.Merchant.name,
        model_merchant.Merchant.location
    )
    
    # --- PASSO 6: Ordenação
    query = query.order_by(total_spent.desc().nullslast())
    
    # --- PASSO 7: Executar
    results = query.all()
    
    # O Pydantic vai mapear os resultados (com 'id', 'name', 'location',
    # 'total_spent', 'receipt_count') para o teu schema 'MerchantReportData'.
    return results

#
# TO-DO (A FAZER) - Funções de Relatório para o Dashboard Principal
# (Os 3 cartões em 'image_157b8d.jpg')
#

def get_dashboard_kpis(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> dict:
    """
    Calcula os 3 KPIs (Key Performance Indicators) para o ecrã principal.
    1. Total Gasto (Month)
    2. Total de Recibos
    3. Total de Produtos
    """
    
    # TO-DO (A FAZER): Esta é uma query complexa que tem de
    # 1. Aplicar os filtros de data
    # 2. Fazer um SUM(price*qty)
    # 3. Fazer um COUNT(receipts.id)
    # 4. Fazer um COUNT(products.id)
    
    # Por agora, devolve dados 'mock' (simulados)
    return {
        "total_spent": Decimal("1234.56"),
        "receipt_count": 12,
        "product_item_count": 156
    }
