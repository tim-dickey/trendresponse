"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.database import init_db
from src.routers import auth, comments, feed, health, users

logger = structlog.get_logger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan context manager."""
    logger.info("Starting TrendResponse application", version="0.1.0")

    # Initialize database
    await init_db()
    logger.info("Database initialized")

    # Initialize Sentry if configured
    if settings.sentry_dsn:
        import sentry_sdk

        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            environment=settings.environment,
            traces_sample_rate=1.0 if settings.environment == "development" else 0.1,
        )
        logger.info("Sentry initialized")

    yield

    logger.info("Shutting down TrendResponse application")


app = FastAPI(
    title="TrendResponse API",
    description="AI-powered social media rapid-response platform",
    version="0.1.0",
    lifespan=lifespan,
    debug=settings.debug,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.environment == "development" else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(feed.router, prefix="/feed", tags=["feed"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
app.include_router(users.router, prefix="/user", tags=["users"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "TrendResponse API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }
