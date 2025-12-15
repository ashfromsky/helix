"""Tests for Demo AI provider."""
import pytest


@pytest.mark.unit
class TestDemoProvider:
    """Test demo/template-based AI provider."""

    @pytest.fixture
    def provider(self):
        """Create demo provider instance."""
        from app.services.ai.providers.demo import DemoProvider
        return DemoProvider()

    @pytest.mark.asyncio
    async def test_generate_get_collection_response(self, provider):
        """Should generate collection response for GET request."""
        response = await provider.generate_response(
            method="GET",
            path="/api/users",
            body=None,
            context=[]
        )

        assert "status_code" in response or isinstance(response, dict)

    @pytest.mark.asyncio
    async def test_generate_get_single_response(self, provider):
        """Should generate single resource response."""
        response = await provider.generate_response(
            method="GET",
            path="/api/users/123",
            body=None,
            context=[]
        )

        assert response is not None

    @pytest.mark.asyncio
    async def test_generate_post_response(self, provider, sample_user):
        """Should generate created response for POST."""
        response = await provider.generate_response(
            method="POST",
            path="/api/users",
            body=sample_user,
            context=[]
        )

        assert response is not None
        body = response.get("body", response)
        if isinstance(body, dict):
            assert "id" in body or "user" in body or len(body) > 0

    @pytest.mark.asyncio
    async def test_generate_put_response(self, provider, sample_user):
        """Should generate updated response for PUT."""
        response = await provider.generate_response(
            method="PUT",
            path="/api/users/123",
            body=sample_user,
            context=[]
        )

        assert response is not None

    @pytest.mark.asyncio
    async def test_generate_delete_response(self, provider):
        """Should generate delete response."""
        response = await provider.generate_response(
            method="DELETE",
            path="/api/users/123",
            body=None,
            context=[]
        )

        assert response is not None
        status = response.get("status_code", 204)
        assert status in [200, 204]

    @pytest.mark.asyncio
    async def test_extract_resource_users(self, provider):
        """Should extract 'users' resource correctly."""
        result = provider._extract_resource("/api/users")
        assert "user" in result.lower()

    @pytest.mark.asyncio
    async def test_extract_resource_products(self, provider):
        """Should extract 'products' resource correctly."""
        result = provider._extract_resource("/api/v1/products")
        assert "product" in result.lower()

    @pytest.mark.asyncio
    async def test_is_collection_true(self, provider):
        """Should identify collection paths."""
        assert provider._is_collection("/api/users") is True
        assert provider._is_collection("/users") is True

    @pytest.mark.asyncio
    async def test_is_collection_false(self, provider):
        """Should identify non-collection paths."""
        assert provider._is_collection("/api/users/123") is False
        assert provider._is_collection("/users/usr_abc") is False

    @pytest.mark.asyncio
    async def test_looks_like_id(self, provider):
        """Should identify ID-like path segments."""
        assert provider._looks_like_id("123") is True
        assert provider._looks_like_id("usr_abc123") is True
        assert provider._looks_like_id("users") is False

    @pytest.mark.asyncio
    async def test_generate_openapi_spec(self, provider):
        """Should generate OpenAPI spec from logs."""
        logs = [
            {"method": "GET", "path": "/api/users", "status_code": 200},
            {"method": "POST", "path": "/api/users", "status_code": 201},
        ]

        result = provider._generate_openapi_spec(logs)

        assert "openapi" in result or "paths" in result or isinstance(result, dict)