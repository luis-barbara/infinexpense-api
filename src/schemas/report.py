from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import List

# A generic schema that serves both "Spending by Category" and "Spending by Merchant".
class ReportSpendingByEntity(BaseModel):
    entity_id: int = Field(description="ID of the entity (e.g., category_id or merchant_id)")
    name: str = Field(description="Name of the entity (e.g., 'Fruit' or 'Continente')")

    # Decimal(12, 2) for money, aligned with the receipt "total_price"
    total_spent: Decimal = Field(
        max_digits=12, 
        decimal_places=2, 
        description="Total amount spent on this entity"
    )

    

# combine base merchant data (from the "Merchant" model) with calculated data
class MerchantReportData(BaseModel):
    # Data from the "model.Merchant"
    id: int
    name: str
    location: str | None = None 
    
    # Calculated Data (services.reports_service.py)
    total_spent: Decimal = Field(
        max_digits=12, 
        decimal_places=2, 
        description="Total amount spent at this merchant"
    )
    receipt_count: int = Field(description="Number of receipts from this merchant")

