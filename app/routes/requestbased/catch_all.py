from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.services.ai.manager import ai_manager
from app.services.cache import cache_service
from app.services.context import context_manager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["catch_all"])


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def handle_request(path: str, request: Request):
    """
    Catch-all handler for all API requests
    Generates mock responses using AI or cache
    """
    try:
        method = request.method

        body = None
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.json()
            except:
                body = None

        session_id = request.headers.get("X-Session-ID", "default")

        cache_key = cache_service.get_cache_key(session_id, method, path, body)
        cached = await cache_service.get(cache_key)
        if cached:
            logger.info(f"Cache HIT: {method} /{path}")
            return JSONResponse(
                status_code=cached.get("status_code", 200),
                content=cached.get("body", {}),
                headers=cached.get("headers", {})
            )

        context = await context_manager.get_context(session_id)

        logger.info(f"Generating response: {method} /{path}")
        response = await ai_manager.generate_response(method, path, body, context)

        await cache_service.set(cache_key, response)

        await context_manager.add_to_context(session_id, {
            "method": method,
            "path": path,
            "body": body,
            "response": response
        })

        return JSONResponse(
            status_code=response.get("status_code", 200),
            content=response.get("body", {}),
            headers=response.get("headers", {})
        )

    except Exception as e:
        logger.error(f"Error handling request: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": str(e)
            }
        )