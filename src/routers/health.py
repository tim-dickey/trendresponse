"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "TrendResponse API"}


@router.get("/metrics")
async def metrics():
    """Prometheus-style metrics endpoint."""
    return {"active_users": 0, "total_comments": 0, "uptime_seconds": 0}
