"""
Tests for the main FastAPI application.
"""
from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint_returns_200(client):
    """Test that health endpoint returns 200 status code."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_endpoint_response_structure(client):
    """Test that health endpoint returns correct JSON structure."""
    response = client.get("/health")
    data = response.json()

    # Check that response has required fields
    assert "status" in data
    assert "timestamp" in data

    # Check that status is "ok"
    assert data["status"] == "ok"

    # Check that timestamp is a valid ISO8601 format
    timestamp = data["timestamp"]
    assert isinstance(timestamp, str)

    # Validate timestamp can be parsed as ISO8601
    try:
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        pytest.fail(f"Timestamp '{timestamp}' is not in valid ISO8601 format")


def test_display_endpoint_returns_200(client):
    """Test that /display endpoint returns 200 status code."""
    response = client.get("/display")
    assert response.status_code == 200


def test_display_endpoint_serves_html(client):
    """Test that /display endpoint serves HTML content."""
    response = client.get("/display")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_display_endpoint_contains_carousel_elements(client):
    """Test that /display endpoint HTML contains required carousel elements."""
    response = client.get("/display")
    html_content = response.text

    # Check for carousel container
    assert "carousel-container" in html_content

    # Check for image elements
    assert "image-primary" in html_content
    assert "image-secondary" in html_content

    # Check for JS and CSS references
    assert "/carousel-ui/js/app.js" in html_content
    assert "/carousel-ui/css/style.css" in html_content
