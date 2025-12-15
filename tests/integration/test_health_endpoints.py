"""Integration tests for health endpoints."""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestHealthEndpoints:
    """Test health and status endpoints."""

    def test_health_endpoint_returns_200(self, client:  TestClient):
        """Health endpoint should return 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_json(self, client: TestClient):
        """Health endpoint should return JSON."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_health_response_has_status(self, client: TestClient):
        """Health response should include status field."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data

    def test_health_status_is_healthy(self, client: TestClient):
        """Health status should be healthy."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] in ["healthy", "ok", "up"]

    def test_status_endpoint_returns_200(self, client: TestClient):
        """Status endpoint should return 200."""
        response = client.get("/status")
        assert response.status_code == 200

    def test_status_includes_version(self, client: TestClient):
        """Status should include version info."""
        response = client.get("/status")
        data = response.json()
        assert "version" in data or "status" in data

    def test_status_includes_ai_provider(self, client: TestClient):
        """Status should include AI provider info."""
        response = client.get("/status")
        data = response.json()
        assert "ai" in data or "provider" in data or "status" in data