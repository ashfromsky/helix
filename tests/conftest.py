import os
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_env_vars():
    """Fixture to mock environment variables."""
    env_vars = {
        "DATABASE_URL": "sqlite:///test.db",
        "SECRET_KEY": "test-secret-key-12345",
        "DEBUG": "true",
    }
    with patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture
def sample_data():
    """Fixture providing sample test data."""
    return {
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com"
        },
        "project": {
            "id": 1,
            "name": "Test Project",
            "description":  "A test project"
        }
    }