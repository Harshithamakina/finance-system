from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from app.models.transaction import TransactionType, TransactionCategory


class TransactionCreate(BaseModel):
    """Schema for creating a new transaction."""
    amount: float = Field(..., gt=0, description="Amount must be greater than 0")
    type: TransactionType
    category: TransactionCategory
    description: Optional[str] = Field(None, max_length=500)
    date: Optional[datetime] = None

    @validator("date", pre=True, always=True)
    def set_date(cls, v):
        return v or datetime.utcnow()


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction."""
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[TransactionType] = None
    category: Optional[TransactionCategory] = None
    description: Optional[str] = Field(None, max_length=500)
    date: Optional[datetime] = None


class TransactionResponse(BaseModel):
    """Schema for returning transaction data."""
    id: int
    amount: float
    type: TransactionType
    category: TransactionCategory
    description: Optional[str]
    date: datetime
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True


class TransactionFilter(BaseModel):
    """Schema for filtering transactions."""
    type: Optional[TransactionType] = None
    category: Optional[TransactionCategory] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_amount: Optional[float] = Field(None, gt=0)
    max_amount: Optional[float] = Field(None, gt=0)