from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status
from datetime import datetime
from app.models.transaction import Transaction
from app.models.user import UserRole
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionFilter


def create_transaction(
    db: Session,
    transaction_data: TransactionCreate,
    user_id: int
) -> Transaction:
    """Create a new transaction."""
    new_transaction = Transaction(
        amount=transaction_data.amount,
        type=transaction_data.type,
        category=transaction_data.category,
        description=transaction_data.description,
        date=transaction_data.date or datetime.utcnow(),
        user_id=user_id
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


def get_transactions(
    db: Session,
    user_id: int,
    user_role: UserRole,
    filters: TransactionFilter = None,
    skip: int = 0,
    limit: int = 20
) -> dict:
    """
    Get transactions with optional filters.
    Admin sees all transactions.
    Others see only their own.
    """
    # Admins see all, others see only their own
    if user_role == UserRole.ADMIN:
        query = db.query(Transaction)
    else:
        query = db.query(Transaction).filter(
            Transaction.user_id == user_id
        )

    # Apply filters if provided
    if filters:
        if filters.type:
            query = query.filter(Transaction.type == filters.type)
        if filters.category:
            query = query.filter(Transaction.category == filters.category)
        if filters.start_date:
            query = query.filter(Transaction.date >= filters.start_date)
        if filters.end_date:
            query = query.filter(Transaction.date <= filters.end_date)
        if filters.min_amount:
            query = query.filter(Transaction.amount >= filters.min_amount)
        if filters.max_amount:
            query = query.filter(Transaction.amount <= filters.max_amount)

    # Get total count before pagination
    total = query.count()

    # Apply pagination
    transactions = query.order_by(
        Transaction.date.desc()
    ).offset(skip).limit(limit).all()

    return {
        "total": total,
        "page": skip // limit + 1,
        "per_page": limit,
        "transactions": transactions
    }


def get_transaction_by_id(
    db: Session,
    transaction_id: int,
    user_id: int,
    user_role: UserRole
) -> Transaction:
    """Get a single transaction by ID."""
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    # Non admins can only view their own transactions
    if user_role != UserRole.ADMIN and transaction.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return transaction


def update_transaction(
    db: Session,
    transaction_id: int,
    update_data: TransactionUpdate,
    user_id: int,
    user_role: UserRole
) -> Transaction:
    """Update an existing transaction."""
    transaction = get_transaction_by_id(
        db, transaction_id, user_id, user_role
    )

    # Only admin and owner can update
    if user_role != UserRole.ADMIN and transaction.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own transactions"
        )

    # Update only provided fields
    update_fields = update_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(transaction, field, value)

    transaction.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(transaction)

    return transaction


def delete_transaction(
    db: Session,
    transaction_id: int,
    user_id: int,
    user_role: UserRole
) -> dict:
    """Delete a transaction."""
    transaction = get_transaction_by_id(
        db, transaction_id, user_id, user_role
    )

    # Only admin can delete any, others only their own
    if user_role != UserRole.ADMIN and transaction.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own transactions"
        )

    db.delete(transaction)
    db.commit()

    return {"message": "Transaction deleted successfully"}