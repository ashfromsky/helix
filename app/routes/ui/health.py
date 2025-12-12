from fastapi import APIRouter
from app.database.core.connect import ping_redis
from app.services.ai.manager import ai_manager
from datetime import datetime

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    redis_healthy = ping_redis()
    ai_status = ai_manager.get_status()

    return {
        "status": "healthy" if redis_healthy else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "redis": "up" if redis_healthy else "down",
            "ai_provider": ai_status["provider"],
            "ai_model": ai_status["model"]
        }
    }


@router.get("/status")
async def detailed_status():
    """Detailed status endpoint"""
    redis_healthy = ping_redis()
    ai_status = ai_manager.get_status()

    return {
        "version": "0.1.0",
        "status": "operational",
        "redis": {
            "connected": redis_healthy,
            "status": "up" if redis_healthy else "down"
        },
        "ai": {
            "provider": ai_status["provider"],
            "model": ai_status["model"],
            "fallback_enabled": ai_status["fallback_enabled"],
            "available_providers": ai_status["available_providers"]
        }
    }