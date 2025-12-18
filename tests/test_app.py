import pytest
import os


class TestConfiguration:
    """Tests for application configuration."""

    def test_env_example_exists(self):
        """Test that .env. example file exists."""
        assert os.path.exists(".env.example"), ".env.example should exist"

    def test_dockerfile_exists(self):
        """Test that Dockerfile exists."""
        assert os.path.exists("Dockerfile"), "Dockerfile should exist"

    def test_docker_compose_exists(self):
        """Test that docker-compose. yml exists."""
        assert os.path.exists("docker-compose.yml"), "docker-compose.yml should exist"


class TestBasicFunctionality:
    """Basic functionality tests."""

    def test_app_directory_exists(self):
        """Test that app directory exists."""
        assert os.path.isdir("app"), "app directory should exist"

    def test_templates_directory_exists(self):
        """Test that templates directory exists."""
        assert os.path.isdir("templates"), "templates directory should exist"


class TestEnvironmentVariables:
    """Tests for environment variable handling."""

    def test_mock_env_vars(self, mock_env_vars):
        """Test that environment variables can be mocked."""
        assert os.environ.get("DATABASE_URL") == "sqlite:///test.db"
        assert os.environ.get("SECRET_KEY") == "test-secret-key-12345"
        assert os.environ.get("DEBUG") == "true"


class TestSampleData:
    """Tests using sample data fixture."""

    def test_sample_user_data(self, sample_data):
        """Test sample user data structure."""
        user = sample_data["user"]
        assert "id" in user
        assert "username" in user
        assert "email" in user
        assert "@" in user["email"]

    def test_sample_project_data(self, sample_data):
        """Test sample project data structure."""
        project = sample_data["project"]
        assert "id" in project
        assert "name" in project
        assert len(project["name"]) > 0
