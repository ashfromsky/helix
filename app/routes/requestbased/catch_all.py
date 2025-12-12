from fastapi import APIRouter, Request

router = APIRouter(tags=["catch_all"])

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def handle_request(path: str, request: Request):
