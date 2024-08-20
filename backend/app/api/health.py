"""
Health check endpoints
"""

from fastapi import APIRouter
from app.models import HealthResponse
from app.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        components={
            "api": "healthy",
            "vector_store": "healthy",
            "llm": "healthy"
        }
    )
