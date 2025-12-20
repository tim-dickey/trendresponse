"""Database models and setup."""

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.config import get_settings

settings = get_settings()


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all database models."""

    pass


class CommentStatus(str, Enum):
    """Comment status enum."""

    DRAFT = "draft"
    POSTING = "posting"
    POSTED = "posted"
    FAILED = "failed"


class User(Base):
    """User model."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    credentials: Mapped[list["PlatformCredential"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    preferences: Mapped[Optional["UserPreferences"]] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class PlatformCredential(Base):
    """Platform credentials model (encrypted tokens)."""

    __tablename__ = "platform_credentials"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    platform: Mapped[str] = mapped_column(String(50))  # 'linkedin', 'twitter', etc.
    access_token: Mapped[str] = mapped_column(Text)  # Encrypted
    refresh_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Encrypted
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="credentials")


class Post(Base):
    """Cached social media post."""

    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)  # Platform-specific ID
    platform: Mapped[str] = mapped_column(String(50), index=True)
    author_id: Mapped[str] = mapped_column(String(255))
    author_name: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    engagement_count: Mapped[int] = mapped_column(Integer, default=0)
    posted_at: Mapped[datetime] = mapped_column(DateTime)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")


class Comment(Base):
    """User-posted comment."""

    __tablename__ = "comments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    post_id: Mapped[str] = mapped_column(ForeignKey("posts.id"), index=True)
    platform: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(String(255))  # 10-25 words enforced
    word_count: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20), default=CommentStatus.DRAFT)
    posted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    platform_response: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")


class UserPreferences(Base):
    """User preferences."""

    __tablename__ = "user_preferences"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), primary_key=True, index=True
    )
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    batch_mode_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    max_words: Mapped[int] = mapped_column(Integer, default=25)
    min_words: Mapped[int] = mapped_column(Integer, default=10)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="preferences")


# Database engine and session
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """Get database session dependency."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
