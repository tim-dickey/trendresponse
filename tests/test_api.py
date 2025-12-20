"""Test API endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data

    def test_metrics(self, client: TestClient):
        """Test metrics endpoint."""
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "active_users" in data
        assert "total_comments" in data

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "TrendResponse API"
        assert data["status"] == "running"


class TestValidationEndpoint:
    """Test comment validation endpoint."""

    @pytest.mark.skip(reason="Requires authentication - implement in integration tests")
    def test_validate_valid_comment(self, client: TestClient):
        """Test validation of valid comment."""
        response = client.post(
            "/comments/validate",
            json={
                "content": "This is a valid comment with exactly fifteen words in total for validation"
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True

    @pytest.mark.skip(reason="Requires authentication - implement in integration tests")
    def test_validate_short_comment(self, client: TestClient):
        """Test validation of too short comment."""
        response = client.post(
            "/comments/validate", json={"content": "Too short"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False
