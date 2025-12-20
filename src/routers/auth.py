"""Authentication router."""

from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_settings
from src.database import User, get_db

router = APIRouter()
settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    email: str
    id: str


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user


@router.post("/linkedin/callback")
async def linkedin_callback(code: str, db: AsyncSession = Depends(get_db)):
    """Handle LinkedIn OAuth callback.

    TODO: Implement actual LinkedIn OAuth token exchange.
    This is a placeholder for the MVP.
    """
    # In production, exchange code for access token with LinkedIn
    # For now, this is a stub
    return {
        "message": "LinkedIn authentication callback",
        "code": code,
        "status": "TODO: Implement token exchange",
    }


@router.post("/logout")
async def logout(current_user: Annotated[User, Depends(get_current_user)]):
    """Logout endpoint (client should discard token)."""
    return {"message": "Successfully logged out"}


@router.get("/status")
async def auth_status(current_user: Annotated[User, Depends(get_current_user)]):
    """Check authentication status."""
    return {"authenticated": True, "user": {"email": current_user.email, "id": str(current_user.id)}}
