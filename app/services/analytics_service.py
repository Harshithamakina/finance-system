from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models.transaction import Transaction, TransactionType
from app.models.user import UserRole
from app.core.config import settings


def calculate_financial_health_score(
    total_income: float,
    total_expenses: float
) -> dict:
    """
    Calculate a financial health score out of 100.
    This is our unique feature that sets us apart.
    """
    if total_income == 0:
        return {
            "score": 0,
            "grade": "F",
            "message": "No income recorded"
        }

    savings_rate = (total_income - total_expenses) / total_income

    # Calculate score based on savings rate
    if savings_rate >= 0.5:
        score = 100
        grade = "A+"
        message = "Excellent! You are saving more than 50% of your income."
    elif savings_rate >= 0.3:
        score = 85
        grade = "A"
        message = "Great! You are saving 30-50% of your income."
    elif savings_rate >= 0.2:
        score = 70
        grade = "B"
        message = "Good. You are saving 20-30% of your income."
    elif savings_rate >= 0.1:
        score = 50
        grade = "C"
        message = "Fair. Try to save at least 20% of your income."
    elif savings_rate >= 0:
        score = 30
        grade = "D"
        message = "Warning. You are barely saving anything."
    else:
        score = 10
        grade = "F"
        message = "Critical! Your expenses exceed your income."

    # Spending alert
    expense_rate = total_expenses / total_income
    alert = None
    if expense_rate >= settings.WARNING_EXPENSE_RATE:
        alert = f"Alert: Your expenses are {expense_rate * 100:.1f}% of your income!"

    return {
        "score": score,
        "grade": grade,
        "message": message,
        "savings_rate": round(savings_rate * 100, 2),
        "alert": alert
    }


def get_summary(db: Session, user_id: int, user_role: UserRole) -> dict:
    """Get full financial summary."""
    # Admins see all, others see their own
    if user_role == UserRole.ADMIN:
        query = db.query(Transaction)
    else:
        query = db.query(Transaction).filter(
            Transaction.user_id == user_id
        )

    transactions = query.all()

    total_income = sum(
        t.amount for t in transactions
        if t.type == TransactionType.INCOME
    )
    total_expenses = sum(
        t.amount for t in transactions
        if t.type == TransactionType.EXPENSE
    )
    balance = total_income - total_expenses
    health = calculate_financial_health_score(total_income, total_expenses)

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "balance": round(balance, 2),
        "total_transactions": len(transactions),
        "financial_health": health
    }


def get_category_breakdown(
    db: Session,
    user_id: int,
    user_role: UserRole
) -> dict:
    """Get spending breakdown by category."""
    if user_role == UserRole.ADMIN:
        query = db.query(Transaction)
    else:
        query = db.query(Transaction).filter(
            Transaction.user_id == user_id
        )

    transactions = query.all()

    breakdown = {}
    for t in transactions:
        category = t.category.value
        if category not in breakdown:
            breakdown[category] = {"total": 0, "count": 0, "type": t.type.value}
        breakdown[category]["total"] += t.amount
        breakdown[category]["count"] += 1

    # Sort by total amount descending
    sorted_breakdown = dict(
        sorted(breakdown.items(), key=lambda x: x[1]["total"], reverse=True)
    )

    return {"category_breakdown": sorted_breakdown}


def get_monthly_summary(
    db: Session,
    user_id: int,
    user_role: UserRole
) -> dict:
    """Get month wise income and expense totals."""
    if user_role == UserRole.ADMIN:
        query = db.query(Transaction)
    else:
        query = db.query(Transaction).filter(
            Transaction.user_id == user_id
        )

    transactions = query.all()

    monthly = {}
    for t in transactions:
        month_key = t.date.strftime("%Y-%m")
        if month_key not in monthly:
            monthly[month_key] = {"income": 0, "expenses": 0, "balance": 0}
        if t.type == TransactionType.INCOME:
            monthly[month_key]["income"] += t.amount
        else:
            monthly[month_key]["expenses"] += t.amount
        monthly[month_key]["balance"] = (
            monthly[month_key]["income"] - monthly[month_key]["expenses"]
        )

    # Sort by month
    sorted_monthly = dict(sorted(monthly.items(), reverse=True))

    return {"monthly_summary": sorted_monthly}


def get_recent_activity(
    db: Session,
    user_id: int,
    user_role: UserRole,
    days: int = 7
) -> dict:
    """Get recent transactions within last N days."""
    since = datetime.utcnow() - timedelta(days=days)

    if user_role == UserRole.ADMIN:
        query = db.query(Transaction).filter(Transaction.date >= since)
    else:
        query = db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.date >= since
        )

    transactions = query.order_by(Transaction.date.desc()).all()

    return {
        "period_days": days,
        "recent_transactions": [
            {
                "id": t.id,
                "amount": t.amount,
                "type": t.type.value,
                "category": t.category.value,
                "description": t.description,
                "date": t.date.isoformat()
            }
            for t in transactions
        ]
    }