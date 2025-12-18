from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.logger import logger_service

router = APIRouter(tags=["Dashboard"])
templates = Jinja2Templates(directory="templates")


@router.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("default_pages/dashboard.html", {"request": request})


@router.get("/api/system/logs")
async def return_logs(limit: int = 50):
    logs = logger_service.get_recent_logs(limit)
    return logs


@router.delete("/api/system/logs")
async def clear_logs():
    logger_service.clear_logs()
    return {"status": "success", "message": "Logs cleared."}
