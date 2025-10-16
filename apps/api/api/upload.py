"""
Photo upload API endpoint.

Handles multipart/form-data photo uploads with validation for format and size.
"""
import logging
import re
import time
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from core.config import RAW_IMAGES_DIR

# Configure logging
logger = logging.getLogger(__name__)

# Router instance
router = APIRouter()

# Constants
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB in bytes
ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.heic']


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to prevent path traversal and other security issues.

    Removes path separators, directory traversal sequences, and dangerous characters.
    Preserves the file extension and basic alphanumeric characters.

    Args:
        filename: Original filename from upload

    Returns:
        Sanitized filename safe for storage
    """
    # Remove any path components (handles both forward and backward slashes)
    filename = Path(filename).name

    # Remove directory traversal sequences
    filename = filename.replace("..", "")

    # Replace any remaining problematic characters with underscores
    # Keep only alphanumeric, dots, hyphens, and underscores
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

    return filename


@router.post("/api/upload", tags=["Upload"])
async def upload_photo(photo: UploadFile = File(...)) -> JSONResponse:
    """
    Upload a photo file.

    Args:
        photo: Uploaded file from multipart/form-data

    Returns:
        JSONResponse with success status and filename

    Raises:
        HTTPException: For validation failures or I/O errors
    """
    # Handle missing file
    if not photo:
        logger.warning("Upload rejected - missing photo field")
        raise HTTPException(
            status_code=400,
            detail={"error": "Missing photo field"}
        )

    # Get original filename
    original_filename = photo.filename
    if not original_filename:
        logger.warning("Upload rejected - missing filename")
        raise HTTPException(
            status_code=400,
            detail={"error": "Missing filename"}
        )

    # Validate file format
    file_extension = Path(original_filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        logger.warning(
            f"Upload rejected - invalid format: {original_filename}, "
            f"extension: {file_extension}"
        )
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid file format",
                "accepted_formats": ["jpeg", "png", "heic"]
            }
        )

    # Read file content
    try:
        contents = await photo.read()
    except Exception as e:
        logger.error(f"Failed to read file: {original_filename}, error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"error": "Failed to read uploaded file"}
        )

    # Validate file size
    file_size = len(contents)
    if file_size > MAX_FILE_SIZE:
        logger.warning(
            f"Upload rejected - file too large: {original_filename}, "
            f"size: {file_size} bytes"
        )
        raise HTTPException(
            status_code=413,
            detail={
                "error": "File too large",
                "max_size_mb": 25
            }
        )

    # Sanitize original filename to prevent path traversal
    safe_filename = sanitize_filename(original_filename)

    # Generate unique temporary filename
    timestamp = int(time.time_ns())
    random_suffix = uuid.uuid4().hex[:8]
    temp_filename = f"{timestamp}_{random_suffix}_{safe_filename}"

    # Save file (directory created by app lifespan on startup)
    file_path = RAW_IMAGES_DIR / temp_filename
    try:
        with open(file_path, 'wb') as f:
            f.write(contents)
        logger.info(
            f"Photo uploaded successfully: {original_filename}, "
            f"size: {file_size} bytes, saved as: {temp_filename}"
        )
    except Exception as e:
        logger.error(
            f"Failed to save file: {original_filename}, "
            f"path: {file_path}, error: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail={"error": "Failed to save uploaded file"}
        )

    # Return success response
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "Photo uploaded successfully",
            "filename": original_filename
        }
    )
