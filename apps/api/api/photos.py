"""
Photo display API endpoint.

Handles fetching photos from the display_images directory.
"""
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from core.config import DISPLAY_IMAGES_DIR

# Configure logging
logger = logging.getLogger(__name__)

# Router instance
router = APIRouter()


class Photo(BaseModel):
    """Photo object structure for API response."""
    id: str
    url: str
    createdAt: str


@router.get("/api/photos", tags=["Photos"])
async def get_photos() -> List[Photo]:
    """
    Get all photos from display_images directory.

    Returns photos sorted chronologically by file modification time (oldest first).

    Returns:
        List[Photo]: Array of photo objects with id, url, and createdAt
    """
    photos = []

    try:
        # Check if directory exists
        if not DISPLAY_IMAGES_DIR.exists():
            logger.warning(f"Display images directory does not exist: {DISPLAY_IMAGES_DIR}")
            return photos

        # Get all image files from display_images directory
        image_extensions = {'.jpg', '.jpeg', '.png', '.heic'}
        image_files = [
            f for f in DISPLAY_IMAGES_DIR.iterdir()
            if f.is_file() and f.suffix.lower() in image_extensions
        ]

        # Sort by modification time (oldest first)
        image_files.sort(key=lambda f: f.stat().st_mtime)

        # Build photo objects
        for image_file in image_files:
            # Get file modification time
            mtime = image_file.stat().st_mtime
            created_at = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()

            # Create photo object
            photo = Photo(
                id=str(uuid.uuid4()),
                url=f"/images/{image_file.name}",
                createdAt=created_at
            )
            photos.append(photo)

        logger.info(f"Fetched {len(photos)} photos from display_images directory")

    except Exception as e:
        logger.error(f"Error fetching photos: {str(e)}")
        # Return empty list on error
        return photos

    return photos
