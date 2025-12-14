from app.services.logger import logger_service
from app.services.ai.manager import ai_manager

async def give_recent_logs(limit: int = 100):
    logs_string = logger_service.get_raw_logs_as_string_wlimit(limit=limit)

    architect_prompt = """
    You are an expert API Architect. 
    Reverse-engineer an OpenAPI 3.0 specification from the provided request logs.

    CRITICAL INSTRUCTIONS:
    1. Analyze the 'raw_logs' provided in the body.
    2. Group similar paths (e.g. /users/1 and /users/2 -> /users/{id}).
    3. Infer data types for request/response bodies.
    4. Return ONLY the valid JSON of the OpenAPI spec.
    """

    response = await ai_manager.generate_response(
        method="INTERNAL",
        path="/generate_openapi",
        body={
            "info": "Attempting to generate OpenAPI spec",
            "raw_logs": logs_string
        },
        system_prompt=architect_prompt
    )

    return response.get("body", {})