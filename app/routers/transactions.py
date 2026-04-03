from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionFilter
)
from app.services.transaction_service import (
    create_transaction,
    get_transactions,
    get_transaction_by_id,
    update_transaction,
    delete_transaction
)
from app.core.dependencies import get_current_user, require_admin
from app.models.user import User
from app.models.transaction import TransactionType, TransactionCategory

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionResponse, status_code=201)
def create(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new transaction."""
    return create_transaction(db, transaction_data, current_user.id)


@router.get("/")
def get_all(
    type: Optional[TransactionType] = Query(None),
    category: Optional[TransactionCategory] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all transactions with optional filters and pagination."""
    filters = TransactionFilter(
        type=type,
        category=category,
        start_date=start_date,
        end_date=end_date,
        min_amount=min_amount,
        max_amount=max_amount
    )
    return get_transactions(
        db, current_user.id, current_user.role, filters, skip, limit
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_one(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single transaction by ID."""
    return get_transaction_by_id(
        db, transaction_id, current_user.id, current_user.role
    )


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update(
    transaction_id: int,
    update_data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a transaction."""
    return update_transaction(
        db, transaction_id, update_data, current_user.id, current_user.role
    )


@router.delete("/{transaction_id}")
def delete(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a transaction."""
    return delete_transaction(
        db, transaction_id, current_user.id, current_user.role
    )