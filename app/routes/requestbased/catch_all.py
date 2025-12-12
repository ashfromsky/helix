from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
import hashlib
import json

from app.services.ai.manager import AIManager
from app.services.cache import CacheService
from app.database.core.config import settings

router = APIRouter()
ai_manager = AIManager()
cache = CacheService()


async def get_request_fingerprint(method: str, path: str, body: bytes) -> str:
    raw = f"{method}:{path}"
    return hashlib.md5(raw.encode()).hexdigest()


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def catch_all_handler(path: str, request: Request):
    method = request.method

    body_bytes = await request.body()
    try:
        body_json = json.loads(body_bytes) if body_bytes else None
    except json.JSONDecodeError:
        body_json = None

    fingerprint = await get_request_fingerprint(method, path, body_bytes)
    cached_response = await cache.get(fingerprint)

    if cached_response:
        data = json.loads(cached_response)
        return JSONResponse(content=data["body"], status_code=data["status_code"])

    system_instruction = "You are a mock server. Generate realistic JSON response."
    user_query = f"Method: {method}, Path: /{path}, Body: {body_json}"

    try:
        ai_result_raw = await ai_manager.generate(system_instruction, user_query)

        try:
            ai_data = json.loads(ai_result_raw)
            status_code = ai_data.get("status_code", 200)
            response_body = ai_data.get("body", ai_data)
        except json.JSONDecodeError:
            status_code = 200
            response_body = {"message": ai_result_raw}

        to_cache = {
            "status_code": status_code,
            "body": response_body
        }
        await cache.set(fingerprint, json.dumps(to_cache))

        return JSONResponse(content=response_body, status_code=status_code)

    except Exception as e:
        return JSONResponse(
            content={"error": "AI Generation Failed", "detail": str(e)},
            status_code=500
        )