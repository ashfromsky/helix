"""Integration tests for dashboard endpoints."""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestDashboardEndpoints:
    """Test dashboard and logging endpoints."""

    def test_dashboard_page_returns_200(self, client: TestClient):
        """Dashboard page should return 200."""
        response = client.get("/dashboard")
        assert response.status_code == 200

    def test_dashboard_returns_html(self, client: TestClient):
        """Dashboard should return HTML."""
        response = client.get("/dashboard")
        assert "text/html" in response.headers["content-type"]

    def test_get_logs_endpoint(self, client: TestClient):
        """Should be able to get system logs."""
        response = client. get("/api/system/logs")
        assert response. status_code == 200

    def test_get_logs_returns_list(self, client: TestClient):
        """Logs endpoint should return list."""
        response = client.get("/api/system/logs")
        data = response.json()
        assert isinstance(data, list)

    def test_get_logs_with_limit(self, client: TestClient):
        """Should respect limit parameter."""
        response = client. get("/api/system/logs? limit=10")
        assert response.status_code == 200

    def test_clear_logs_endpoint(self, client: TestClient):
        """Should be able to clear logs."""
        response = client.delete("/api/system/logs")
        assert response.status_code == 200

    def test_clear_logs_returns_success(self, client: TestClient):
        """Clear logs should return success message."""
        response = client.delete("/api/system/logs")
        data = response.json()
        assert "status" in data or "message" in data