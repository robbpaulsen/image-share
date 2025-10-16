"""
Centralized configuration for the Image Share API.

This module provides centralized access to configuration values,
following the "Variables de Entorno Centralizadas" coding standard.
"""
from pathlib import Path

# Image directories configuration
# Future: Make configurable via environment variables
IMAGE_DATA_ROOT = Path("/image-share-data")
RAW_IMAGES_DIR = IMAGE_DATA_ROOT / "raw_images"
DISPLAY_IMAGES_DIR = IMAGE_DATA_ROOT / "display_images"
FAILED_IMAGES_DIR = IMAGE_DATA_ROOT / "failed_images"
