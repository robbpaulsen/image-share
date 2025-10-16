"""
Tests for the photos API endpoint.
"""
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from core.config import DISPLAY_IMAGES_DIR
from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_images(tmp_path, monkeypatch):
    """
    Create temporary test images and patch DISPLAY_IMAGES_DIR.

    Creates three test image files with different modification times.
    """
    # Create a temporary directory for test images
    test_dir = tmp_path / "test_display_images"
    test_dir.mkdir()

    # Patch the DISPLAY_IMAGES_DIR configuration
    monkeypatch.setattr("core.config.DISPLAY_IMAGES_DIR", test_dir)
    monkeypatch.setattr("api.photos.DISPLAY_IMAGES_DIR", test_dir)

    # Create test image files with different modification times
    image1 = test_dir / "photo1.jpg"
    image2 = test_dir / "photo2.png"
    image3 = test_dir / "photo3.jpeg"

    # Create files with staggered creation times (oldest first)
    image1.write_bytes(b"fake image 1 content")
    time.sleep(0.01)  # Small delay to ensure different mtimes

    image2.write_bytes(b"fake image 2 content")
    time.sleep(0.01)

    image3.write_bytes(b"fake image 3 content")

    return test_dir, [image1, image2, image3]


def test_get_photos_returns_200(client):
    """Test that /api/photos endpoint returns 200 status code."""
    response = client.get("/api/photos")
    assert response.status_code == 200


def test_get_photos_returns_array(client):
    """Test that /api/photos endpoint returns a JSON array."""
    response = client.get("/api/photos")
    data = response.json()
    assert isinstance(data, list)


def test_get_photos_empty_directory(client, tmp_path, monkeypatch):
    """Test that /api/photos returns empty array when no images exist."""
    # Create empty directory
    empty_dir = tmp_path / "empty_display_images"
    empty_dir.mkdir()

    # Patch configuration
    monkeypatch.setattr("core.config.DISPLAY_IMAGES_DIR", empty_dir)
    monkeypatch.setattr("api.photos.DISPLAY_IMAGES_DIR", empty_dir)

    response = client.get("/api/photos")
    data = response.json()

    assert response.status_code == 200
    assert data == []


def test_get_photos_structure(client, test_images):
    """Test that /api/photos returns correct photo object structure."""
    response = client.get("/api/photos")
    data = response.json()

    assert len(data) == 3

    # Check first photo structure
    photo = data[0]
    assert "id" in photo
    assert "url" in photo
    assert "createdAt" in photo

    # Validate field types
    assert isinstance(photo["id"], str)
    assert isinstance(photo["url"], str)
    assert isinstance(photo["createdAt"], str)

    # Validate URL format
    assert photo["url"].startswith("/images/")
    assert photo["url"].endswith((".jpg", ".png", ".jpeg"))


def test_get_photos_chronological_order(client, test_images):
    """Test that photos are sorted by modification time (oldest first)."""
    test_dir, image_files = test_images

    response = client.get("/api/photos")
    data = response.json()

    assert len(data) == 3

    # Extract filenames from URLs
    returned_filenames = [photo["url"].split("/")[-1] for photo in data]

    # Expected order: photo1.jpg, photo2.png, photo3.jpeg (oldest to newest)
    expected_filenames = ["photo1.jpg", "photo2.png", "photo3.jpeg"]

    assert returned_filenames == expected_filenames


def test_get_photos_ignores_non_images(client, tmp_path, monkeypatch):
    """Test that /api/photos ignores non-image files."""
    # Create directory with mixed files
    mixed_dir = tmp_path / "mixed_display_images"
    mixed_dir.mkdir()

    # Create image and non-image files
    (mixed_dir / "photo1.jpg").write_bytes(b"image content")
    (mixed_dir / "document.txt").write_bytes(b"text content")
    (mixed_dir / "data.json").write_bytes(b'{"key": "value"}')
    (mixed_dir / "photo2.png").write_bytes(b"image content 2")

    # Patch configuration
    monkeypatch.setattr("core.config.DISPLAY_IMAGES_DIR", mixed_dir)
    monkeypatch.setattr("api.photos.DISPLAY_IMAGES_DIR", mixed_dir)

    response = client.get("/api/photos")
    data = response.json()

    # Should only return the 2 image files
    assert len(data) == 2

    # Verify only image URLs are returned
    urls = [photo["url"] for photo in data]
    assert all(url.split("/")[-1] in ["photo1.jpg", "photo2.png"] for url in urls)
