# src/routers/reports.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import logging

# Importa as dependências (DB, Service, Schemas de resposta)
from src.db.dependencies import get_db
from src.services import reports_service 
from src.schemas import report as schema_report  


router = APIRouter(
    prefix="/reports",  
    tags=["Reports"] 
)


# Endpoint: Relatório de Gastos por Categoria (para o gráfico)
@router.get(
    "/spending-by-category",
    response_model=List[schema_report.ReportSpendingByEntity]
)
def get_spending_by_category_endpoint(
    # filtros de data que frontend vai enviar
    start_date: Optional[date] = Query(default=None, description="Data de início (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(default=None, description="Data de fim (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Obtém o relatório de total gasto por categoria, com filtro de data.
    Usado para o gráfico no Dashboard e no ecrã de Categorias.
    """
    try:
        report_data = reports_service.get_spending_by_category(
            db=db,
            start_date=start_date,
            end_date=end_date
        )
        return report_data
    except Exception as e:
        # Qualquer erro inesperado da query SQL complexa
        logging.error(f"Erro ao gerar 'spending-by-category' report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao calcular o relatório."
        )


# Endpoint: "Analytics"" de Supermercados 
@router.get(
    "/enriched-merchants",
    response_model=List[schema_report.MerchantReportData]
)
def get_enriched_merchant_report_endpoint(
    # filtros
    start_date: Optional[date] = Query(default=None, description="Data de início (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(default=None, description="Data de fim (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Obtém a lista de supermercados "enriquecida" com o total gasto
    e a contagem de recibos.
    Usado no ecrã de 'Configurações -> Gerir Supermercados'.
    """
    try:
        report_data = reports_service.get_enriched_merchant_report(
            db=db,
            start_date=start_date,
            end_date=end_date
        )
        return report_data
    except Exception as e:
        logging.error(f"Erro ao gerar 'enriched-merchant' report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao calcular o relatório de supermercados."
        )


# Endpoint : KPIs do Dashboard (os 3 cartões)
@router.get(
    "/dashboard-kpis",
    response_model=dict  # Devolve um dicionário simples
)
def get_dashboard_kpis_endpoint(
    start_date: Optional[date] = Query(default=None, description="Data de início (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(default=None, description="Data de fim (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Obtém os 3 KPIs (Key Performance Indicators) para o topo
    do dashboard ('image_157b8d.jpg').
    """
    try:
        kpi_data = reports_service.get_dashboard_kpis(
            db=db,
            start_date=start_date,
            end_date=end_date
        )
        return kpi_data
    except Exception as e:
        logging.error(f"Erro ao gerar 'dashboard-kpis' report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao calcular os KPIs do dashboard."
        )