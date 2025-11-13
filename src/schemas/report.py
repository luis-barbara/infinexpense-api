# src/schemas/report.py

from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import List

#
# --- Schema para os Gráficos do Dashboard (Ecrã 1 / 'image_157b8d.jpg') ---
#
class ReportSpendingByEntity(BaseModel):
    """
    Um schema genérico que serve tanto para "Gastos por Categoria"
    como para "Gastos por Supermercado".
    Representa um único item num gráfico de barras ou circular.
    """
    entity_id: int = Field(description="ID of the entity (e.g., category_id or merchant_id)")
    name: str = Field(description="Name of the entity (e.g., 'Dairy' or 'Continente')")
    
    total_spent: Decimal = Field(
        max_digits=12, 
        decimal_places=2, 
        description="Total amount spent on this entity"
    )

    # model_config = ConfigDict(from_attributes=True) # Precisamos disto!
    model_config = ConfigDict(from_attributes=True)


# ---
# Schema para a Lista Enriquecida de Supermercados (Ecrã 4 / 'image_b893b5.png')
# ---
class MerchantReportData(BaseModel):
    """
    Schema para a lista de supermercados no ecrã de Configurações.
    Combina os dados base do supermercado ('model' Merchant) com dados calculados.
    """
    # Dados que vêm do 'model.Merchant'
    id: int
    name: str
    location: str | None = None # Mantém o 'location' que definimos
    
    # Dados Calculados (que o 'reports_service.py' vai calcular)
    total_spent: Decimal = Field(
        max_digits=12, 
        decimal_places=2, 
        description="Total amount spent at this merchant"
    )
    receipt_count: int = Field(description="Number of receipts from this merchant")

    # model_config = ConfigDict(from_attributes=True) # Precisamos disto!
    model_config = ConfigDict(from_attributes=True)
