from fastapi import APIRouter, Request
from app.services.ai.manager import ai_manager
from app.services.cache import cache_service
from app.services.context import context_manager

router = APIRouter(tags=["catch_all"])


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def handle_request(path: str, request: Request):
    method = request.method
    body = await request.json() if request.method in ["POST", "PUT", "PATCH"] else None
    session_id = request.headers.get("X-Session-ID", "default")

    cache_key = cache_service.get_cache_key(session_id, method, path, body)
    cached = await cache_service.get(cache_key)
    if cached:
        return cached

    context = await context_manager.get_context(session_id)

    response = await ai_manager.generate_response(method, path, body, context)

    await cache_service.set(cache_key, response)

    await context_manager.add_to_context(session_id, {
        "method": method, "path": path, "body": body, "response": response
    })

    return response