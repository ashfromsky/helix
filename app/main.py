import random
import logging
import asyncio

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes.ui import default as ui_routes
from app.routes.ui import health
from app.routes.requestbased import catch_all
from app.database.core.config import settings
from app.services.ai.config import ai_settings
app = FastAPI(
    title="MockPilot",
    description="AI-Powered API Mocking Platform",
    version="1.0.0"
)

logger = logging.getLogger("uvicorn.error")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(health.router, tags=["Health"])
app.include_router(ui_routes.router, tags=["UI"])

app.include_router(catch_all.router, tags=["Mocking"])

@app.middleware("http")
async def chaos_middleware(request: Request, call_next):
    if not getattr(ai_settings, "CHAOS_ENABLED", False):
        return await call_next(request)

    if request.url.path.startswith(("/docs", "/redoc", "/openapi.json", "/health")):
        return await call_next(request)

    if random.random() < getattr(ai_settings, "CHAOS_LATENCY_RATE", 0.0):
        min_delay = getattr(ai_settings, "CHAOS_MIN_DELAY", 100) / 1000
        max_delay = getattr(ai_settings, "CHAOS_MAX_DELAY", 2000) / 1000
        delay = random.uniform(min_delay, max_delay)
        logger.warning(f"🐌 Chaos: Adding delay {delay:.2f}s to {request.url.path}")
        await asyncio.sleep(delay)

    if random.random() < getattr(ai_settings, "CHAOS_ERROR_RATE", 0.0):
        logger.error(f"💥 Chaos: Injecting 500 error to {request.url.path}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Chaos Monkey Strike",
                "message": "Simulated infrastructure failure by Helix"
            }
        )

    response = await call_next(request)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

