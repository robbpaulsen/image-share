"""
Photo Processing Pipeline Module.

This module monitors the raw_images directory and processes uploaded photos:
- Generates UUID v4 filenames for deduplication
- Corrects EXIF orientation metadata
- Moves processed images to display_images directory
- Handles errors by moving failed images to failed_images directory

Follows the backend architecture pattern defined in architecture/section-11.
"""
import asyncio
import logging
import time
import uuid
from pathlib import Path
from typing import Optional

from PIL import Image, ImageOps, UnidentifiedImageError

from core.config import (
    RAW_IMAGES_DIR,
    DISPLAY_IMAGES_DIR,
    FAILED_IMAGES_DIR,
)

# Configure logger for processor module
logger = logging.getLogger("image_processor")
logger.setLevel(logging.INFO)

# Log format: timestamp, level, module, message
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Log to stdout (captured by systemd journald in production)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Constants
MAX_CONCURRENT_PROCESSING = 5
MONITORING_INTERVAL_SECONDS = 10

# Track files currently being processed to prevent duplicate processing
_processing_files: set[str] = set()


class PhotoProcessor:
    """
    Photo processor class to encapsulate processing logic.

    Handles UUID generation, EXIF orientation correction, and file management.
    """

    @staticmethod
    def generate_uuid_filename(original_filename: str) -> tuple[str, str]:
        """
        Generate UUID v4 filename preserving original format.

        Args:
            original_filename: Original filename with extension

        Returns:
            Tuple of (uuid_filename, original_filename) for logging
        """
        # Extract file extension from original filename
        extension = Path(original_filename).suffix.lower()

        # Generate UUID v4
        unique_id = uuid.uuid4()
        uuid_filename = f"{unique_id}{extension}"

        logger.info(f"Renamed {original_filename} → {uuid_filename}")

        return uuid_filename, original_filename

    @staticmethod
    def correct_image_orientation(image: Image.Image) -> tuple[Image.Image, bool]:
        """
        Apply EXIF orientation correction to image using PIL's standard method.

        Uses ImageOps.exif_transpose() which correctly handles all 8 EXIF
        orientation values and automatically removes the orientation tag after
        applying the correction.

        Args:
            image: PIL Image object

        Returns:
            Tuple of (corrected_image, was_corrected)
            was_corrected is True if orientation correction was applied
        """
        try:
            # Use PIL's built-in EXIF orientation handler
            # This handles all 8 orientation values correctly and removes the tag
            corrected = ImageOps.exif_transpose(image)

            # exif_transpose returns None if no correction was needed
            if corrected is not None:
                return corrected, True

            # No correction needed (orientation was 1 or missing)
            return image, False

        except Exception as e:
            # If EXIF reading fails, return original image
            logger.warning(f"Failed to read EXIF data: {e}")
            return image, False

    @staticmethod
    async def process_single_image(image_path: Path) -> bool:
        """
        Process a single image through the complete pipeline.

        Steps:
        1. Generate UUID filename
        2. Open image and correct EXIF orientation
        3. Save to display_images directory
        4. Delete original from raw_images
        5. On error: move to failed_images

        Args:
            image_path: Path to image in raw_images directory

        Returns:
            True on success, False on failure
        """
        start_time = time.time()
        original_filename = image_path.name

        try:
            # Mark file as being processed
            _processing_files.add(original_filename)

            logger.info(f"Processing: {original_filename}")

            # Generate UUID filename
            uuid_filename, _ = PhotoProcessor.generate_uuid_filename(original_filename)

            # Run blocking I/O operations in thread pool to avoid blocking event loop
            def process_image():
                # Open image
                image = Image.open(image_path)

                # Correct orientation
                corrected_image, was_corrected = PhotoProcessor.correct_image_orientation(image)

                if was_corrected:
                    logger.info(f"Applied EXIF orientation correction to {uuid_filename}")

                # Save to display_images directory with UUID filename
                output_path = DISPLAY_IMAGES_DIR / uuid_filename

                # Preserve original format
                # Extract format from extension or image format
                image_format = image.format or Path(original_filename).suffix[1:].upper()
                if image_format == 'JPG':
                    image_format = 'JPEG'

                corrected_image.save(output_path, format=image_format)

                return output_path

            # Execute in thread pool
            output_path = await asyncio.to_thread(process_image)

            # Delete original file from raw_images
            image_path.unlink()

            # Calculate processing duration
            duration_ms = int((time.time() - start_time) * 1000)
            logger.info(f"Successfully processed {original_filename} in {duration_ms}ms")

            return True

        except UnidentifiedImageError as e:
            logger.error(f"Corrupted image: {original_filename} - {e}")
            await PhotoProcessor._move_to_failed(image_path, original_filename)
            return False

        except Exception as e:
            logger.error(f"Unexpected error processing {original_filename}: {type(e).__name__} - {e}")
            await PhotoProcessor._move_to_failed(image_path, original_filename)
            return False

        finally:
            # Remove from processing set
            _processing_files.discard(original_filename)

    @staticmethod
    async def _move_to_failed(image_path: Path, original_filename: str) -> None:
        """
        Move failed image to failed_images directory.

        Args:
            image_path: Path to failed image
            original_filename: Original filename for logging
        """
        try:
            if image_path.exists():
                failed_path = FAILED_IMAGES_DIR / original_filename
                await asyncio.to_thread(image_path.rename, failed_path)
                logger.info(f"Moved failed image {original_filename} to failed_images/")
        except Exception as e:
            logger.error(f"Failed to move {original_filename} to failed_images/: {e}")


async def process_batch(image_files: list[Path]) -> list[bool]:
    """
    Process multiple images concurrently with limit.

    Processes up to MAX_CONCURRENT_PROCESSING images at once.

    Args:
        image_files: List of image file paths to process

    Returns:
        List of success/failure booleans for each file
    """
    # Limit to MAX_CONCURRENT_PROCESSING files
    files_to_process = image_files[:MAX_CONCURRENT_PROCESSING]

    # Create tasks for concurrent processing
    tasks = [PhotoProcessor.process_single_image(img) for img in files_to_process]

    # Gather results, capturing exceptions
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Convert exceptions to False
    return [r if isinstance(r, bool) else False for r in results]


async def monitor_raw_images() -> None:
    """
    Monitor raw_images directory every 10 seconds for new files.

    Background task that continuously monitors for new images and
    processes them through the photo processing pipeline.

    This function runs indefinitely until cancelled by FastAPI shutdown.
    """
    logger.info("Photo processor started - monitoring raw_images/")

    while True:
        try:
            # Find new image files
            image_files = []
            for pattern in ['*.jpg', '*.jpeg', '*.png', '*.heic']:
                image_files.extend(RAW_IMAGES_DIR.glob(pattern))

            # Filter out files currently being processed
            new_files = [f for f in image_files if f.name not in _processing_files]

            if new_files:
                logger.info(f"Monitoring raw_images/ - Found {len(new_files)} new files")
                await process_batch(new_files)

            # Poll every 10 seconds
            await asyncio.sleep(MONITORING_INTERVAL_SECONDS)

        except asyncio.CancelledError:
            logger.info("Photo processor shutdown requested")
            raise

        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}")
            # Continue monitoring even on error
            await asyncio.sleep(MONITORING_INTERVAL_SECONDS)
