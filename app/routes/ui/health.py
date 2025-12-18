from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.database.core.connect import ping_redis
from app.services.ai.manager import ai_manager

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
            "ai_model": ai_status["model"],
        },
    }


@router.get("/status")
async def detailed_status():
    """
    Проверка состояния сервиса и его компонентов.
    """
    try:
        # Вызов метода get_status, который вызывал ошибку ранее
        ai_status = ai_manager.get_status()

        return {
            "service": "Helix Backend",
            "status": "online",
            "version": "0.1.0",
            "components": {"ai_manager": ai_status, "database": "connected"},
        }
    except Exception as e:
        print(f"Health check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
