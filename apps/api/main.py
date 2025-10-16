"""
FastAPI application for Image Share.

Provides endpoints for photo upload, display, and health checking.
"""
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.photos import router as photos_router
from api.upload import router as upload_router
from core.config import DISPLAY_IMAGES_DIR, FAILED_IMAGES_DIR, RAW_IMAGES_DIR

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.

    Handles startup and shutdown tasks:
    - Creates required image directories on startup
    """
    # Startup: Create image directories
    for directory in [RAW_IMAGES_DIR, DISPLAY_IMAGES_DIR, FAILED_IMAGES_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured directory exists: {directory}")

    yield

    # Shutdown: cleanup tasks (if needed in future)
    logger.info("Application shutting down")


# Create FastAPI application
app = FastAPI(
    title="Image Share API",
    description="API for uploading and displaying event photos",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(upload_router)
app.include_router(photos_router)

# Mount static files for serving display images
app.mount("/images", StaticFiles(directory=str(DISPLAY_IMAGES_DIR)), name="images")

# Mount carousel-ui static files (JS, CSS)
CAROUSEL_UI_DIR = Path(__file__).parent.parent / "carousel-ui"
app.mount("/carousel-ui", StaticFiles(directory=str(CAROUSEL_UI_DIR)), name="carousel-ui")


@app.get("/display", tags=["Carousel"])
async def serve_carousel():
    """
    Serve the carousel display page.

    Returns:
        FileResponse: The carousel HTML page
    """
    carousel_html = CAROUSEL_UI_DIR / "index.html"
    return FileResponse(carousel_html)


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Status and timestamp information
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
