from sqlalchemy.orm import Session
from sqlalchemy import func, case, distinct
from decimal import Decimal
from typing import List, Optional
from datetime import date

from src.models import (
    merchant as model_merchant,
    receipt as model_receipt,
    product as model_product_list,
    receipt_product as model_receipt_product,
    category as model_category
)
from src.schemas import reports as schema_reports


def get_spending_by_category(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[schema_reports.ReportSpendingByEntity]:
    """Get total spending by category for the dashboard chart."""
    total_item_spend = (model_receipt_product.Product.price * model_receipt_product.Product.quantity).label("total_item_spend") 
    query = db.query(
        model_category.Category.id.label("entity_id"),
        model_category.Category.name.label("name"),
        func.coalesce(func.sum(total_item_spend), Decimal("0.00")).label("total_spent")
    )

    query = query.join(
        model_product_list.ProductList,
        model_category.Category.id == model_product_list.ProductList.category_id,
        isouter=True
    )
    query = query.join(
        model_receipt_product.Product,
        model_product_list.ProductList.id == model_receipt_product.Product.product_list_id,
        isouter=True
    )
    query = query.join(
        model_receipt.Receipt,
        model_receipt_product.Product.receipt_id == model_receipt.Receipt.id,
        isouter=True
    )

    if start_date:
        query = query.filter(model_receipt.Receipt.purchase_date >= start_date)
    if end_date:
        query = query.filter(model_receipt.Receipt.purchase_date <= end_date)

    query = query.group_by(model_category.Category.id, model_category.Category.name)
    query = query.order_by(func.sum(total_item_spend).desc().nullslast())

    return query.all()


def get_enriched_merchant_report(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[schema_reports.MerchantReportData]:
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

    # Criar uma SubQuery para os Recibos JÁ FILTRADOS por data
    # crucial para o LEFT JOIN funcionar
    
    filtered_receipts_subq = db.query(
        model_receipt.Receipt.id,
        model_receipt.Receipt.merchant_id
    ).filter(model_receipt.Receipt.id != None) 

    if start_date:
        filtered_receipts_subq = filtered_receipts_subq.filter(
            model_receipt.Receipt.purchase_date >= start_date
        )
    if end_date:
        filtered_receipts_subq = filtered_receipts_subq.filter(
            model_receipt.Receipt.purchase_date <= end_date
        )
    
    # Transforma a query numa "tabela" que podemos usar num JOIN
    filtered_receipts_subq = filtered_receipts_subq.subquery()

    # Definir os cálculos
    # Total Gasto (SUM)
    total_spent = func.coalesce(
        func.sum(model_receipt_product.Product.price * model_receipt_product.Product.quantity),
        Decimal("0.00")
    ).label("total_spent")
    
    # Contagem de Recibos (COUNT)
    receipt_count = func.count(
        func.distinct(filtered_receipts_subq.c.id)
    ).label("receipt_count")

    # Query Principal (a partir do Merchant)
    
    query = db.query(
        model_merchant.Merchant.id,
        model_merchant.Merchant.name,
        model_merchant.Merchant.location,
        total_spent,
        receipt_count
    )
    
    # LEFT JOINs
    
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
    
    # Agrupamento (GROUP BY)
    # Agrupa pelo Supermercado
    query = query.group_by(
        model_merchant.Merchant.id,
        model_merchant.Merchant.name,
        model_merchant.Merchant.location
    )
    
    # Ordenação
    query = query.order_by(total_spent.desc().nullslast())
    
    # Executar
    results = query.all()
    
    return results


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
    
    # 1. Define o cálculo do preço total por item (preço * quantidade)
    total_item_spent = (model_receipt_product.Product.price * model_receipt_product.Product.quantity).label("total_item_spent")
    
    # 2. Inicia a query
    query = db.query(
        # Total gasto (soma de preço * quantidade de todos os produtos)
        func.coalesce(func.sum(total_item_spent), Decimal("0.00")).label("total_spent"),
        
        # Contagem de recibos distintos
        func.count(distinct(model_receipt.Receipt.id)).label("receipt_count"),
        
        # Contagem de produtos distintos
        func.count(distinct(model_receipt_product.Product.id)).label("product_item_count")
    )
    
    # 3.  JOINs necessários
    query = query.join(
        model_receipt_product.Product,
        model_receipt_product.Product.receipt_id == model_receipt.Receipt.id
    )

    # 4. Filtros 
    if start_date:
        query = query.filter(model_receipt.Receipt.purchase_date >= start_date)
    if end_date:
        query = query.filter(model_receipt.Receipt.purchase_date <= end_date)

    # 5. Executa a query
    result = query.one()  
    
    # 6. Retorna os KPIs calculados
    return {
        "total_spent": result.total_spent,
        "receipt_count": result.receipt_count,
        "product_item_count": result.product_item_count
    }