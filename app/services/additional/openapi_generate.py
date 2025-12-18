from app.services.ai.manager import ai_manager
from app.services.logger import logger_service


async def give_recent_logs(limit: int = 100):
    logs = logger_service.get_recent_logs(limit=limit)

    if not logs:
        return {"error": "No logs available", "message": "Make some API requests first to generate traffic data"}

    architect_prompt = """You are an expert OpenAPI 3.0 specification architect.

Your task: Analyze the provided API request logs and generate a complete OpenAPI 3.0 specification.

CRITICAL REQUIREMENTS:
1. **Group similar paths**: /users/1 and /users/2 → /users/{id}
2. **Infer schemas**: Analyze response bodies to determine data types
3. **REST conventions**: Follow standard HTTP method semantics
4. **Valid JSON**: Output MUST be valid OpenAPI 3.0 JSON format
5. **No markdown**: Do NOT wrap output in ```json``` code blocks

RESPONSE FORMAT (STRICT):
{
  "status_code": 200,
  "headers": {"Content-Type": "application/json"},
  "body": {
    "openapi": "3.0.0",
    "info": {
      "title": "Generated API",
      "version": "1.0.0",
      "description": "Auto-generated from Helix traffic logs"
    },
    "servers": [{"url": "http://localhost:8080"}],
    "paths": {
      "/api/users": {
        "get": {
          "summary": "List users",
          "responses": {
            "200": {
              "description": "Success",
              "content": {
                "application/json": {
                  "schema": {"type": "object"}
                }
              }
            }
          }
        }
      }
    }
  }
}

Analyze the logs below and generate the OpenAPI spec:"""

    response = await ai_manager.generate_response(
        method="POST",
        path="/api/generate-spec",
        body={"task": "generate_openapi_spec", "logs": logs, "log_count": len(logs)},
        system_prompt=architect_prompt,
    )

    body = response.get("body", {})

    if "openapi" in body:
        return body
    elif isinstance(body, dict) and "body" in body:
        return body.get("body", {})
    else:
        return {
            "error": "Failed to generate OpenAPI spec",
            "raw_response": body,
            "hint": "AI provider may not support system prompts. Try using DeepSeek or Groq.",
        }
