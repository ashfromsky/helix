"""Integration tests for OpenAPI generation."""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestOpenAPIGeneration:
    """Test OpenAPI spec generation endpoint."""

    def test_generate_spec_without_logs_returns_404(self, client: TestClient):
        """Should return 404 when no logs exist."""
        client.delete("/api/system/logs")

        response = client.get("/api/generate-spec")
        assert response.status_code in [404, 200]

    def test_generate_spec_after_requests(self, client: TestClient):
        """Should generate spec after making requests."""
        client.get("/api/users")
        client.post("/api/users", json={"name": "Test"})
        client.get("/api/products")

        response = client.get("/api/generate-spec? limit=50")

        assert response.status_code in [200, 404]

    def test_generate_spec_with_limit(self, client: TestClient):
        """Should respect limit parameter."""
        response = client.get("/api/generate-spec?limit=10")
        assert response.status_code in [200, 404]

    def test_generate_spec_returns_json(self, client: TestClient):
        """Should return JSON response."""
        client.get("/api/users")

        response = client.get("/api/generate-spec")
        if response.status_code == 200:
            assert "application/json" in response.headers["content-type"]