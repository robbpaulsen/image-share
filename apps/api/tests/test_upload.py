"""
Unit tests for photo upload endpoint.

Tests cover:
- Valid uploads (JPEG, PNG, HEIC)
- File size validation
- File format validation
- Missing file field handling
- File collision prevention
"""
import io
import pytest
from fastapi.testclient import TestClient

from main import app
from core.config import RAW_IMAGES_DIR

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_cleanup():
    """Setup test environment and cleanup after tests."""
    # Setup: Ensure raw_images directory exists and clean up all test files
    RAW_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # Pre-test cleanup: Remove all test files from previous runs
    if RAW_IMAGES_DIR.exists():
        for pattern in ["*test*", "*duplicate*", "*photo*", "*large*", "*max*", "*over*", "*document*"]:
            for file in RAW_IMAGES_DIR.glob(pattern):
                file.unlink(missing_ok=True)

    yield

    # Post-test cleanup: Remove test files
    if RAW_IMAGES_DIR.exists():
        for pattern in ["*test*", "*duplicate*", "*photo*", "*large*", "*max*", "*over*", "*document*"]:
            for file in RAW_IMAGES_DIR.glob(pattern):
                file.unlink(missing_ok=True)


def test_upload_valid_jpeg():
    """Test successful upload of valid JPEG file."""
    # Create fake JPEG file
    file_content = b"\xff\xd8\xff\xe0" + b"fake jpeg content" * 100
    files = {"photo": ("test.jpg", io.BytesIO(file_content), "image/jpeg")}

    response = client.post("/api/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Photo uploaded successfully"
    assert data["filename"] == "test.jpg"

    # Verify file was saved
    saved_files = list(RAW_IMAGES_DIR.glob("*test.jpg"))
    assert len(saved_files) == 1


def test_upload_valid_jpeg_alternate_extension():
    """Test successful upload of JPEG with .jpeg extension."""
    file_content = b"\xff\xd8\xff\xe0" + b"fake jpeg content" * 100
    files = {"photo": ("photo.jpeg", io.BytesIO(file_content), "image/jpeg")}

    response = client.post("/api/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["filename"] == "photo.jpeg"


def test_upload_valid_png():
    """Test successful upload of valid PNG file."""
    # PNG file signature
    file_content = b"\x89PNG\r\n\x1a\n" + b"fake png content" * 100
    files = {"photo": ("test.png", io.BytesIO(file_content), "image/png")}

    response = client.post("/api/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Photo uploaded successfully"
    assert data["filename"] == "test.png"


def test_upload_valid_heic():
    """Test successful upload of valid HEIC file."""
    file_content = b"fake heic content" * 100
    files = {"photo": ("test.heic", io.BytesIO(file_content), "image/heic")}

    response = client.post("/api/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["filename"] == "test.heic"


def test_upload_oversized_file():
    """Test rejection of file larger than 25MB."""
    # Create file larger than 25MB
    large_content = b"x" * (26 * 1024 * 1024)  # 26MB
    files = {"photo": ("large.jpg", io.BytesIO(large_content), "image/jpeg")}

    response = client.post("/api/upload", files=files)

    assert response.status_code == 413
    data = response.json()
    assert data["detail"]["error"] == "File too large"
    assert data["detail"]["max_size_mb"] == 25


def test_upload_invalid_format():
    """Test rejection of invalid file format."""
    file_content = b"fake text file content"
    files = {"photo": ("test.txt", io.BytesIO(file_content), "text/plain")}

    response = client.post("/api/upload", files=files)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["error"] == "Invalid file format"
    assert "jpeg" in data["detail"]["accepted_formats"]
    assert "png" in data["detail"]["accepted_formats"]
    assert "heic" in data["detail"]["accepted_formats"]


def test_upload_invalid_format_pdf():
    """Test rejection of PDF file format."""
    file_content = b"%PDF-1.4 fake pdf content"
    files = {"photo": ("document.pdf", io.BytesIO(file_content), "application/pdf")}

    response = client.post("/api/upload", files=files)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["error"] == "Invalid file format"


def test_upload_missing_photo_field():
    """Test error handling when photo field is missing."""
    # Send request without photo field
    response = client.post("/api/upload", files={})

    # FastAPI returns 422 for missing required field
    assert response.status_code == 422


def test_upload_no_file_collisions():
    """Test that multiple uploads with same filename don't collide."""
    file_content = b"fake content" * 100

    # Upload first file
    files1 = {"photo": ("duplicate.jpg", io.BytesIO(file_content), "image/jpeg")}
    response1 = client.post("/api/upload", files=files1)
    assert response1.status_code == 200

    # Upload second file with same name
    files2 = {"photo": ("duplicate.jpg", io.BytesIO(file_content), "image/jpeg")}
    response2 = client.post("/api/upload", files=files2)
    assert response2.status_code == 200

    # Verify both files exist (different temporary filenames)
    saved_files = list(RAW_IMAGES_DIR.glob("*duplicate.jpg"))
    assert len(saved_files) == 2


def test_upload_case_insensitive_extension():
    """Test that file extension validation is case-insensitive."""
    # Test uppercase extension
    file_content = b"fake content" * 100
    files = {"photo": ("test.JPG", io.BytesIO(file_content), "image/jpeg")}

    response = client.post("/api/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_upload_maximum_allowed_size():
    """Test upload of file at exactly 25MB (boundary test)."""
    # Create file exactly 25MB
    max_content = b"x" * (25 * 1024 * 1024)
    files = {"photo": ("max.jpg", io.BytesIO(max_content), "image/jpeg")}

    response = client.post("/api/upload", files=files)

    # Should succeed as it's exactly at the limit
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_upload_just_over_size_limit():
    """Test upload of file just over 25MB (boundary test)."""
    # Create file 25MB + 1 byte
    over_limit = b"x" * (25 * 1024 * 1024 + 1)
    files = {"photo": ("over.jpg", io.BytesIO(over_limit), "image/jpeg")}

    response = client.post("/api/upload", files=files)

    assert response.status_code == 413
    data = response.json()
    assert data["detail"]["error"] == "File too large"
