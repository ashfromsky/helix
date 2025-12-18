"""
Base AI Provider Interface
All AI providers must inherit from this class
"""

import json
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseAIProvider(ABC):
    """
    Abstract base class for all AI providers
    Defines the interface that all providers must implement
    """

    @abstractmethod
    async def generate_response(
        self,
        method: str,
        path: str,
        body: Optional[Dict] = None,
        context: Optional[list] = None,
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate mock API response based on request parameters

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            path: Request path (e.g., /api/v1/users)
            body: Request body (for POST/PUT/PATCH)
            context: Previous requests context for consistency

        Returns:
            Dict with status_code, headers, and body
        """
        pass

    def _get_system_prompt(self) -> str:
        """
        Load system prompt from assets/AI/MOCKPILOT_SYSTEM.md
        """
        try:
            with open("assets/AI/MOCKPILOT_SYSTEM.md", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return """You are MockPilot AI, an intelligent API mocking engine.
Generate realistic JSON responses for API requests.

Rules:
1. Analyze the HTTP method and path
2. Generate realistic data (use real names, emails, dates)
3. Follow REST standards (GET -> array or object, POST -> 201, DELETE -> 204)
4. Use data from request body when provided
5. Keep responses consistent with context

Output ONLY valid JSON in this format:
{
  "status_code": <int>,
  "headers": {"Content-Type": "application/json"},
  "body": <json_data>
}"""

    def _build_user_prompt(
        self, method: str, path: str, body: Optional[Dict] = None, context: Optional[list] = None
    ) -> str:
        """
        Build user prompt with request details
        """
        prompt_parts = [
            f"Method: {method}",
            f"Path: {path}",
        ]

        if body:
            prompt_parts.append(f"Request Body:\n{json.dumps(body, indent=2)}")

        if context and len(context) > 0:
            context_str = "\n".join([f"- {req.get('method')} {req.get('path')}" for req in context[-5:]])
            prompt_parts.append(f"Recent Context:\n{context_str}")

        prompt_parts.append("\nGenerate appropriate JSON response:")

        return "\n\n".join(prompt_parts)

    def _parse_ai_response(self, text: str) -> Dict[str, Any]:
        """
        Parse AI response text and extract JSON
        Handles various formats: markdown code blocks, plain JSON, etc.
        """
        json_match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        code_match = re.search(r"```\s*(\{.*?\})\s*```", text, re.DOTALL)
        if code_match:
            try:
                return json.loads(code_match.group(1))
            except json.JSONDecodeError:
                pass

        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        return {
            "status_code": 500,
            "headers": {"Content-Type": "application/json"},
            "body": {"error": "Failed to parse AI response", "raw_response": text[:200]},
        }

    def _validate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and normalize AI response
        Ensures response has required fields
        """
        if not isinstance(response, dict):
            return {
                "status_code": 500,
                "headers": {"Content-Type": "application/json"},
                "body": {"error": "Invalid response format"},
            }

        response.setdefault("status_code", 200)
        response.setdefault("headers", {"Content-Type": "application/json"})
        response.setdefault("body", {})

        return response
