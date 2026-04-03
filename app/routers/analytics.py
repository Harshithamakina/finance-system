from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analytics_service import (
    get_summary,
    get_category_breakdown,
    get_monthly_summary,
    get_recent_activity
)
from app.core.dependencies import (
    get_current_user,
    require_analyst_or_above
)
from app.models.user import User

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/summary")
def summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get full financial summary with health score."""
    return get_summary(db, current_user.id, current_user.role)


@router.get("/category-breakdown")
def category_breakdown(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_above)
):
    """Get category wise breakdown — analyst and admin only."""
    return get_category_breakdown(db, current_user.id, current_user.role)


@router.get("/monthly")
def monthly_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_above)
):
    """Get month wise summary — analyst and admin only."""
    return get_monthly_summary(db, current_user.id, current_user.role)


@router.get("/recent-activity")
def recent_activity(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recent transactions within last N days."""
    return get_recent_activity(db, current_user.id, current_user.role, days)