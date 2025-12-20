"""Comments router for creating and managing comments."""

from datetime import datetime
from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Comment, CommentStatus, Post, User, get_db
from src.routers.auth import get_current_user
from src.services.suggestions import suggestion_service

router = APIRouter()


class CommentValidationRequest(BaseModel):
    content: str


class CommentValidationResponse(BaseModel):
    valid: bool
    word_count: int
    message: str


class CommentSuggestionRequest(BaseModel):
    post_id: str
    num_suggestions: int = Field(default=3, ge=1, le=5)


class CommentSuggestionResponse(BaseModel):
    suggestions: List[str]


class CommentCreateRequest(BaseModel):
    post_id: str
    content: str
    platform: str = "linkedin"

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate comment content."""
        if not v or not v.strip():
            raise ValueError("Comment content cannot be empty")
        return v.strip()


class CommentResponse(BaseModel):
    id: str
    post_id: str
    platform: str
    content: str
    word_count: int
    status: str
    posted_at: str | None
    created_at: str

    class Config:
        from_attributes = True


@router.post("/validate", response_model=CommentValidationResponse)
async def validate_comment(
    request: CommentValidationRequest,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Validate comment word count and content rules."""
    is_valid, message = suggestion_service.validate_comment(request.content)
    word_count = suggestion_service.count_words(request.content)

    return CommentValidationResponse(
        valid=is_valid,
        word_count=word_count,
        message=message if not is_valid else "Comment is valid",
    )


@router.post("/suggest", response_model=CommentSuggestionResponse)
async def suggest_comments(
    request: CommentSuggestionRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    """Generate AI-powered comment suggestions for a post."""
    # Get the post
    result = await db.execute(select(Post).where(Post.id == request.post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Generate suggestions
    suggestions = await suggestion_service.generate_suggestions(
        post_content=post.content,
        post_author=post.author_name,
        num_suggestions=request.num_suggestions,
    )

    return CommentSuggestionResponse(suggestions=suggestions)


@router.post("/post", response_model=CommentResponse)
async def post_comment(
    request: CommentCreateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    """Post a comment to a social media platform.

    TODO: Implement actual posting to LinkedIn API.
    For now, this stores the comment in the database.
    """
    # Validate comment
    is_valid, message = suggestion_service.validate_comment(request.content)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    # Verify post exists
    result = await db.execute(select(Post).where(Post.id == request.post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Create comment
    word_count = suggestion_service.count_words(request.content)
    comment = Comment(
        user_id=current_user.id,
        post_id=request.post_id,
        platform=request.platform,
        content=request.content,
        word_count=word_count,
        status=CommentStatus.POSTED,  # TODO: Change to POSTING when implementing actual API
        posted_at=datetime.utcnow(),
    )

    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    return CommentResponse(
        id=str(comment.id),
        post_id=comment.post_id,
        platform=comment.platform,
        content=comment.content,
        word_count=comment.word_count,
        status=comment.status,
        posted_at=comment.posted_at.isoformat() if comment.posted_at else None,
        created_at=comment.created_at.isoformat(),
    )


@router.get("/history", response_model=List[CommentResponse])
async def get_comment_history(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
    limit: int = 50,
):
    """Get user's posted comment history."""
    result = await db.execute(
        select(Comment)
        .where(Comment.user_id == current_user.id)
        .order_by(desc(Comment.created_at))
        .limit(limit)
    )
    comments = result.scalars().all()

    return [
        CommentResponse(
            id=str(comment.id),
            post_id=comment.post_id,
            platform=comment.platform,
            content=comment.content,
            word_count=comment.word_count,
            status=comment.status,
            posted_at=comment.posted_at.isoformat() if comment.posted_at else None,
            created_at=comment.created_at.isoformat(),
        )
        for comment in comments
    ]
