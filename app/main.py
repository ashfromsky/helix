from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from app.routes.ui.default import router as default_router
from app.routes.ui.health import router as health_router
from app.routes.requestbased.catch_all import router as catch_all_router
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Helix",
    description="AI-powered API mocking server that generates realistic responses automatically",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "path": str(request.url)
        }
    )


app.include_router(health_router)
app.include_router(default_router)

app.include_router(catch_all_router)

logger.info("Helix server initialized")


@app.on_event("startup")
async def startup_event():
    """Startup event handler - check dependencies"""
    logger.info("=" * 60)
    logger.info("🌀 Starting Helix Server")
    logger.info("=" * 60)

    from app.database.core.connect import ping_redis
    if ping_redis():
        logger.info("✓ Redis connection: OK")
    else:
        logger.warning("✗ Redis connection: FAILED (using in-memory fallback)")

    from app.services.ai.manager import ai_manager
    status = ai_manager.get_status()
    logger.info(f"✓ AI Provider: {status['provider']}")
    logger.info(f"✓ AI Model: {status['model']}")
    logger.info(f"✓ Fallback enabled: {status['fallback_enabled']}")

    available = status['available_providers']
    logger.info("Available AI providers:")
    for provider, is_available in available.items():
        status_icon = "✓" if is_available else "✗"
        logger.info(f"  {status_icon} {provider}")

    logger.info("=" * 60)
    logger.info("🚀 Helix is ready!")
    logger.info("   Web UI: http://localhost:8080")
    logger.info("   Health: http://localhost:8080/health")
    logger.info("   Docs:   http://localhost:8080/docs")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("Shutting down Helix server...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )