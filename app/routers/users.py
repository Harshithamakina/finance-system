from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.user import UserResponse
from app.services.auth_service import get_all_users, deactivate_user
from app.core.dependencies import require_admin, get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get current logged in user profile."""
    return current_user


@router.get("/", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all users — admin only."""
    return get_all_users(db)


@router.patch("/{user_id}/deactivate", response_model=UserResponse)
def deactivate(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Deactivate a user account — admin only."""
    return deactivate_user(db, user_id)