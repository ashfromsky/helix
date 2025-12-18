import time
import json
from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import JSONResponse

from app.services.ai.manager import ai_manager
from app.services.cache import cache_service
from app.services.analyzer import request_analyzer
from app.services.context import context_manager
from app.services.logger import logger_service

router = APIRouter()


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def catch_all_handler(path: str, request: Request, background_tasks: BackgroundTasks):
    start_time = time.time()
    method = request.method
    session_id = request.headers.get("X-Session-ID", "default_session")

    try:
        body = await request.json()
    except:
        body = {}

    cache_key = cache_service.get_cache_key(session_id, method, path, body)
    cached = await cache_service.get(cache_key)
    if cached:
        duration = (time.time() - start_time) * 1000
        background_tasks.add_task(
            logger_service.log_request, method, path, cached["status_code"], duration, body, cached["body"]
        )
        return JSONResponse(content=cached["body"], status_code=cached["status_code"], headers=cached.get("headers"))

    resource = request_analyzer.extract_resource(path)
    operation = request_analyzer.get_operation_type(method, path)

    context = await context_manager.get_context(session_id)

    response_data = await ai_manager.generate_response(method=method, path=path, body=body, context=context)

    await cache_service.set(cache_key, response_data)

    await context_manager.add_to_context(
        session_id, {"method": method, "path": path, "body": body, "response": response_data}
    )

    duration = (time.time() - start_time) * 1000
    background_tasks.add_task(
        logger_service.log_request,
        method,
        path,
        response_data.get("status_code", 200),
        duration,
        body,
        response_data.get("body"),
    )

    return JSONResponse(content=response_data.get("body", {}), status_code=response_data.get("status_code", 200))
