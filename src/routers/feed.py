"""Feed router for trending posts."""

from typing import Annotated, List

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Post, User, get_db
from src.routers.auth import get_current_user

router = APIRouter()


class PostResponse(BaseModel):
    id: str
    platform: str
    author_id: str
    author_name: str
    content: str
    engagement_count: int
    posted_at: str

    class Config:
        from_attributes = True


@router.get("/trending", response_model=List[PostResponse])
async def get_trending_posts(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
    limit: int = Query(50, ge=1, le=100),
    platform: str | None = Query(None, description="Filter by platform (e.g., 'linkedin')"),
):
    """Get trending posts from feed.

    TODO: Implement actual feed aggregation from LinkedIn API.
    This returns cached posts for now.
    """
    query = select(Post).order_by(desc(Post.engagement_count), desc(Post.posted_at)).limit(limit)

    if platform:
        query = query.where(Post.platform == platform)

    result = await db.execute(query)
    posts = result.scalars().all()

    return [
        PostResponse(
            id=post.id,
            platform=post.platform,
            author_id=post.author_id,
            author_name=post.author_name,
            content=post.content,
            engagement_count=post.engagement_count,
            posted_at=post.posted_at.isoformat(),
        )
        for post in posts
    ]


@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post_details(
    post_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    """Get full post details by ID."""
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Post not found")

    return PostResponse(
        id=post.id,
        platform=post.platform,
        author_id=post.author_id,
        author_name=post.author_name,
        content=post.content,
        engagement_count=post.engagement_count,
        posted_at=post.posted_at.isoformat(),
    )
