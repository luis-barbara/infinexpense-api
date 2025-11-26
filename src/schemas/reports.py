from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import List

class ReportSpendingByEntity(BaseModel):
    """
    A generic schema that serves both "Spending by Category"
    and "Spending by Merchant".
    Represents a single item in a bar or pie chart.
    """
    entity_id: int = Field(description="ID of the entity (e.g., category_id or merchant_id)")
    name: str = Field(description="Name of the entity (e.g., 'Dairy' or 'Continente')")
    
    total_spent: Decimal = Field(
        max_digits=12, 
        decimal_places=2, 
        description="Total amount spent on this entity"
    )

    model_config = ConfigDict(from_attributes=True)

class MerchantReportData(BaseModel):
    """
    Schema for the list of merchants in the Settings screen.
    Combines base merchant data ('model' Merchant) with calculated data.
    """
    id: int
    name: str
    location: str | None = None 
    
    total_spent: Decimal = Field(
        max_digits=12, 
        decimal_places=2, 
        description="Total amount spent at this merchant"
    )
    receipt_count: int = Field(description="Number of receipts from this merchant")

    model_config = ConfigDict(from_attributes=True)