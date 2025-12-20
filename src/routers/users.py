"""Users router for user profile and preferences."""

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import User, UserPreferences, get_db
from src.routers.auth import get_current_user

router = APIRouter()


class UserProfileResponse(BaseModel):
    id: str
    email: str
    created_at: str


class UserPreferencesRequest(BaseModel):
    notifications_enabled: bool | None = None
    batch_mode_enabled: bool | None = None
    max_words: int | None = None
    min_words: int | None = None


class UserPreferencesResponse(BaseModel):
    notifications_enabled: bool
    batch_mode_enabled: bool
    max_words: int
    min_words: int


@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Get user profile information."""
    return UserProfileResponse(
        id=str(current_user.id),
        email=current_user.email,
        created_at=current_user.created_at.isoformat(),
    )


@router.get("/preferences", response_model=UserPreferencesResponse)
async def get_user_preferences(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    """Get user preferences."""
    # Get or create preferences
    if not current_user.preferences:
        prefs = UserPreferences(user_id=current_user.id)
        db.add(prefs)
        await db.commit()
        await db.refresh(prefs)
    else:
        prefs = current_user.preferences

    return UserPreferencesResponse(
        notifications_enabled=prefs.notifications_enabled,
        batch_mode_enabled=prefs.batch_mode_enabled,
        max_words=prefs.max_words,
        min_words=prefs.min_words,
    )


@router.put("/preferences", response_model=UserPreferencesResponse)
async def update_user_preferences(
    request: UserPreferencesRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    """Update user preferences."""
    # Get or create preferences
    if not current_user.preferences:
        prefs = UserPreferences(user_id=current_user.id)
        db.add(prefs)
    else:
        prefs = current_user.preferences

    # Update fields if provided
    if request.notifications_enabled is not None:
        prefs.notifications_enabled = request.notifications_enabled
    if request.batch_mode_enabled is not None:
        prefs.batch_mode_enabled = request.batch_mode_enabled
    if request.max_words is not None:
        prefs.max_words = request.max_words
    if request.min_words is not None:
        prefs.min_words = request.min_words

    await db.commit()
    await db.refresh(prefs)

    return UserPreferencesResponse(
        notifications_enabled=prefs.notifications_enabled,
        batch_mode_enabled=prefs.batch_mode_enabled,
        max_words=prefs.max_words,
        min_words=prefs.min_words,
    )
