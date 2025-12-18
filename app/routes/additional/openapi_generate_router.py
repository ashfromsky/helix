from fastapi import APIRouter, HTTPException, Query
from app.services.additional.openapi_generate import give_recent_logs
from app.services.logger import logger_service

router = APIRouter()


@router.get("/api/generate-spec", tags=["OpenAPI Generation"])
async def get_openapi_spec(limit: int = Query(50, ge=10)):
    check_logs = logger_service.get_recent_logs(limit=1)

    if not check_logs:
        raise HTTPException(status_code=404, detail="No traffic recorded yet. Make some requests to the API first.")

    try:
        spec = await give_recent_logs(limit)

        if "openapi" not in spec and "swagger" not in spec:
            return {"error": "AI failed to generate valid spec", "raw": spec}

        return spec

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
