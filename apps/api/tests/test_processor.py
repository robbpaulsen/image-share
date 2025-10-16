"""
Unit tests for photo processor module.

Tests cover:
- UUID generation uniqueness and format
- EXIF orientation parsing and transformation
- File operations (move, delete, save)
- Error handling for corrupted images
- Logging verification
"""
import asyncio
import uuid
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest
from PIL import Image, UnidentifiedImageError

from core.processor import (
    PhotoProcessor,
    process_batch,
    monitor_raw_images,
)


class TestUUIDGeneration:
    """Test UUID generation functionality."""

    def test_uuid_uniqueness(self):
        """Test UUID generation produces unique values across 1000 calls."""
        generated_uuids = set()

        for _ in range(1000):
            uuid_filename, _ = PhotoProcessor.generate_uuid_filename("test.jpg")
            # Extract UUID from filename (remove extension)
            uuid_str = uuid_filename.replace(".jpg", "")
            generated_uuids.add(uuid_str)

        # All 1000 UUIDs should be unique
        assert len(generated_uuids) == 1000

    def test_uuid_filename_format_jpg(self):
        """Test UUID filename format with .jpg extension."""
        uuid_filename, original = PhotoProcessor.generate_uuid_filename("photo.jpg")

        # Should have .jpg extension
        assert uuid_filename.endswith(".jpg")

        # Should be valid UUID v4 format
        uuid_str = uuid_filename.replace(".jpg", "")
        parsed_uuid = uuid.UUID(uuid_str)
        assert parsed_uuid.version == 4

        # Should return original filename
        assert original == "photo.jpg"

    def test_uuid_filename_format_png(self):
        """Test UUID filename format preserves PNG extension."""
        uuid_filename, _ = PhotoProcessor.generate_uuid_filename("image.png")

        assert uuid_filename.endswith(".png")

        uuid_str = uuid_filename.replace(".png", "")
        parsed_uuid = uuid.UUID(uuid_str)
        assert parsed_uuid.version == 4

    def test_uuid_filename_format_heic(self):
        """Test UUID filename format preserves HEIC extension."""
        uuid_filename, _ = PhotoProcessor.generate_uuid_filename("photo.HEIC")

        # Should normalize to lowercase
        assert uuid_filename.endswith(".heic")

        uuid_str = uuid_filename.replace(".heic", "")
        parsed_uuid = uuid.UUID(uuid_str)
        assert parsed_uuid.version == 4


class TestEXIFOrientation:
    """Test EXIF orientation correction functionality."""

    def test_exif_orientation_no_exif(self):
        """Test image without EXIF data returns original image."""
        # Create simple test image without EXIF
        test_image = Image.new('RGB', (100, 100), color='red')

        corrected, orientation = PhotoProcessor.correct_image_orientation(test_image)

        assert corrected == test_image
        assert orientation is None

    def test_exif_orientation_value_1_no_change(self):
        """Test orientation 1 (normal) requires no transformation."""
        test_image = Image.new('RGB', (100, 100), color='blue')

        # Mock getexif to return orientation 1
        with patch.object(test_image, 'getexif') as mock_exif:
            mock_exif.return_value = {274: 1}  # 274 is orientation tag
            corrected, orientation = PhotoProcessor.correct_image_orientation(test_image)

            assert orientation == 1
            # Image should be unchanged for orientation 1
            assert corrected == test_image

    def test_exif_orientation_value_2_flip_horizontal(self):
        """Test orientation 2 applies horizontal flip."""
        test_image = Image.new('RGB', (100, 50), color='green')

        with patch.object(test_image, 'getexif') as mock_exif:
            mock_exif.return_value = {274: 2}

            with patch.object(test_image, 'transpose') as mock_transpose:
                mock_transpose.return_value = test_image
                corrected, orientation = PhotoProcessor.correct_image_orientation(test_image)

                assert orientation == 2
                mock_transpose.assert_called_once_with(Image.FLIP_LEFT_RIGHT)

    def test_exif_orientation_value_3_rotate_180(self):
        """Test orientation 3 applies 180 degree rotation."""
        test_image = Image.new('RGB', (100, 50), color='yellow')

        with patch.object(test_image, 'getexif') as mock_exif:
            mock_exif.return_value = {274: 3}

            with patch.object(test_image, 'rotate') as mock_rotate:
                mock_rotate.return_value = test_image
                corrected, orientation = PhotoProcessor.correct_image_orientation(test_image)

                assert orientation == 3
                mock_rotate.assert_called_once_with(180, expand=True)

    def test_exif_orientation_value_6_rotate_270(self):
        """Test orientation 6 (90 CW) applies 270 degree rotation."""
        test_image = Image.new('RGB', (100, 50), color='purple')

        with patch.object(test_image, 'getexif') as mock_exif:
            mock_exif.return_value = {274: 6}

            with patch.object(test_image, 'rotate') as mock_rotate:
                mock_rotate.return_value = test_image
                corrected, orientation = PhotoProcessor.correct_image_orientation(test_image)

                assert orientation == 6
                mock_rotate.assert_called_once_with(270, expand=True)

    def test_exif_orientation_value_8_rotate_90(self):
        """Test orientation 8 (90 CCW) applies 90 degree rotation."""
        test_image = Image.new('RGB', (100, 50), color='orange')

        with patch.object(test_image, 'getexif') as mock_exif:
            mock_exif.return_value = {274: 8}

            with patch.object(test_image, 'rotate') as mock_rotate:
                mock_rotate.return_value = test_image
                corrected, orientation = PhotoProcessor.correct_image_orientation(test_image)

                assert orientation == 8
                mock_rotate.assert_called_once_with(90, expand=True)

    def test_exif_orientation_exception_handling(self):
        """Test EXIF parsing handles exceptions gracefully."""
        test_image = Image.new('RGB', (100, 50), color='white')

        with patch.object(test_image, 'getexif') as mock_exif:
            mock_exif.side_effect = Exception("EXIF read error")

            corrected, orientation = PhotoProcessor.correct_image_orientation(test_image)

            # Should return original image on exception
            assert corrected == test_image
            assert orientation is None


class TestFileOperations:
    """Test file operation functionality."""

    @pytest.mark.asyncio
    async def test_process_single_image_success(self, tmp_path):
        """Test successful image processing moves file from raw to display."""
        # Create test directories
        raw_dir = tmp_path / "raw_images"
        display_dir = tmp_path / "display_images"
        raw_dir.mkdir()
        display_dir.mkdir()

        # Create test image
        test_image_path = raw_dir / "test_photo.jpg"
        test_image = Image.new('RGB', (100, 100), color='red')
        test_image.save(test_image_path, format='JPEG')

        # Mock config paths
        with patch('core.processor.RAW_IMAGES_DIR', raw_dir):
            with patch('core.processor.DISPLAY_IMAGES_DIR', display_dir):
                result = await PhotoProcessor.process_single_image(test_image_path)

                assert result is True
                # Original file should be deleted
                assert not test_image_path.exists()
                # Display directory should have one file
                display_files = list(display_dir.glob("*.jpg"))
                assert len(display_files) == 1
                # UUID filename format
                uuid_filename = display_files[0].name
                uuid_str = uuid_filename.replace(".jpg", "")
                parsed_uuid = uuid.UUID(uuid_str)
                assert parsed_uuid.version == 4

    @pytest.mark.asyncio
    async def test_process_single_image_corrupted(self, tmp_path):
        """Test corrupted image moves to failed_images directory."""
        # Create test directories
        raw_dir = tmp_path / "raw_images"
        failed_dir = tmp_path / "failed_images"
        display_dir = tmp_path / "display_images"
        raw_dir.mkdir()
        failed_dir.mkdir()
        display_dir.mkdir()

        # Create corrupted file (not a valid image)
        corrupted_path = raw_dir / "corrupted.jpg"
        corrupted_path.write_text("This is not an image")

        # Mock config paths
        with patch('core.processor.RAW_IMAGES_DIR', raw_dir):
            with patch('core.processor.DISPLAY_IMAGES_DIR', display_dir):
                with patch('core.processor.FAILED_IMAGES_DIR', failed_dir):
                    result = await PhotoProcessor.process_single_image(corrupted_path)

                    assert result is False
                    # File should be moved to failed_images
                    failed_files = list(failed_dir.glob("*.jpg"))
                    assert len(failed_files) == 1
                    assert failed_files[0].name == "corrupted.jpg"
                    # Original should not exist
                    assert not corrupted_path.exists()

    @pytest.mark.asyncio
    async def test_process_single_image_preserves_format_png(self, tmp_path):
        """Test processing preserves PNG format."""
        raw_dir = tmp_path / "raw_images"
        display_dir = tmp_path / "display_images"
        raw_dir.mkdir()
        display_dir.mkdir()

        # Create PNG test image
        test_image_path = raw_dir / "test.png"
        test_image = Image.new('RGBA', (100, 100), color='blue')
        test_image.save(test_image_path, format='PNG')

        with patch('core.processor.RAW_IMAGES_DIR', raw_dir):
            with patch('core.processor.DISPLAY_IMAGES_DIR', display_dir):
                result = await PhotoProcessor.process_single_image(test_image_path)

                assert result is True
                # Should have PNG file in display
                display_files = list(display_dir.glob("*.png"))
                assert len(display_files) == 1

    @pytest.mark.asyncio
    async def test_original_file_deletion_after_success(self, tmp_path):
        """Test original file is deleted after successful processing."""
        raw_dir = tmp_path / "raw_images"
        display_dir = tmp_path / "display_images"
        raw_dir.mkdir()
        display_dir.mkdir()

        test_image_path = raw_dir / "delete_me.jpg"
        test_image = Image.new('RGB', (50, 50), color='green')
        test_image.save(test_image_path, format='JPEG')

        with patch('core.processor.RAW_IMAGES_DIR', raw_dir):
            with patch('core.processor.DISPLAY_IMAGES_DIR', display_dir):
                await PhotoProcessor.process_single_image(test_image_path)

                # Original should be deleted
                assert not test_image_path.exists()
                # Only UUID file in display
                assert len(list(raw_dir.glob("*"))) == 0


class TestErrorHandling:
    """Test error handling functionality."""

    @pytest.mark.asyncio
    async def test_unidentified_image_error_handling(self, tmp_path):
        """Test UnidentifiedImageError is caught and handled."""
        raw_dir = tmp_path / "raw_images"
        failed_dir = tmp_path / "failed_images"
        display_dir = tmp_path / "display_images"
        raw_dir.mkdir()
        failed_dir.mkdir()
        display_dir.mkdir()

        bad_file = raw_dir / "bad.jpg"
        bad_file.write_bytes(b"Not an image")

        with patch('core.processor.RAW_IMAGES_DIR', raw_dir):
            with patch('core.processor.DISPLAY_IMAGES_DIR', display_dir):
                with patch('core.processor.FAILED_IMAGES_DIR', failed_dir):
                    result = await PhotoProcessor.process_single_image(bad_file)

                    assert result is False
                    assert (failed_dir / "bad.jpg").exists()

    @pytest.mark.asyncio
    async def test_move_to_failed_on_exception(self, tmp_path):
        """Test unexpected exceptions move file to failed_images."""
        raw_dir = tmp_path / "raw_images"
        failed_dir = tmp_path / "failed_images"
        display_dir = tmp_path / "display_images"
        raw_dir.mkdir()
        failed_dir.mkdir()
        display_dir.mkdir()

        test_file = raw_dir / "test.jpg"
        test_image = Image.new('RGB', (50, 50), color='red')
        test_image.save(test_file, format='JPEG')

        # Force an exception during processing
        with patch('core.processor.RAW_IMAGES_DIR', raw_dir):
            with patch('core.processor.DISPLAY_IMAGES_DIR', display_dir):
                with patch('core.processor.FAILED_IMAGES_DIR', failed_dir):
                    with patch('PIL.Image.open', side_effect=Exception("Unexpected error")):
                        result = await PhotoProcessor.process_single_image(test_file)

                        assert result is False
                        assert (failed_dir / "test.jpg").exists()


class TestLogging:
    """Test logging functionality."""

    @pytest.mark.asyncio
    async def test_uuid_mapping_logged(self, tmp_path, caplog):
        """Test original -> UUID mapping is logged."""
        import logging
        caplog.set_level(logging.INFO)

        original_filename = "vacation_photo.jpg"

        uuid_filename, original = PhotoProcessor.generate_uuid_filename(original_filename)

        # Check log contains mapping
        assert f"Renamed {original_filename} → {uuid_filename}" in caplog.text

    @pytest.mark.asyncio
    async def test_processing_start_logged(self, tmp_path, caplog):
        """Test processing start is logged."""
        import logging
        caplog.set_level(logging.INFO)

        raw_dir = tmp_path / "raw_images"
        display_dir = tmp_path / "display_images"
        raw_dir.mkdir()
        display_dir.mkdir()

        test_file = raw_dir / "logged.jpg"
        test_image = Image.new('RGB', (50, 50), color='blue')
        test_image.save(test_file, format='JPEG')

        with patch('core.processor.RAW_IMAGES_DIR', raw_dir):
            with patch('core.processor.DISPLAY_IMAGES_DIR', display_dir):
                await PhotoProcessor.process_single_image(test_file)

                assert "Processing: logged.jpg" in caplog.text

    @pytest.mark.asyncio
    async def test_error_logged_on_failure(self, tmp_path, caplog):
        """Test errors are logged with appropriate level."""
        import logging
        caplog.set_level(logging.ERROR)

        raw_dir = tmp_path / "raw_images"
        failed_dir = tmp_path / "failed_images"
        display_dir = tmp_path / "display_images"
        raw_dir.mkdir()
        failed_dir.mkdir()
        display_dir.mkdir()

        bad_file = raw_dir / "error.jpg"
        bad_file.write_bytes(b"Invalid")

        with patch('core.processor.RAW_IMAGES_DIR', raw_dir):
            with patch('core.processor.DISPLAY_IMAGES_DIR', display_dir):
                with patch('core.processor.FAILED_IMAGES_DIR', failed_dir):
                    await PhotoProcessor.process_single_image(bad_file)

                    assert "Corrupted image" in caplog.text or "error.jpg" in caplog.text


class TestConcurrency:
    """Test concurrent processing functionality."""

    @pytest.mark.asyncio
    async def test_process_batch_limits_concurrent(self, tmp_path):
        """Test process_batch limits to MAX_CONCURRENT_PROCESSING."""
        raw_dir = tmp_path / "raw_images"
        display_dir = tmp_path / "display_images"
        raw_dir.mkdir()
        display_dir.mkdir()

        # Create 10 test images
        image_files = []
        for i in range(10):
            test_file = raw_dir / f"image_{i}.jpg"
            test_image = Image.new('RGB', (50, 50), color='red')
            test_image.save(test_file, format='JPEG')
            image_files.append(test_file)

        with patch('core.processor.RAW_IMAGES_DIR', raw_dir):
            with patch('core.processor.DISPLAY_IMAGES_DIR', display_dir):
                # Process batch should only handle first 5
                results = await process_batch(image_files)

                # Should return 5 results (MAX_CONCURRENT_PROCESSING)
                assert len(results) == 5

    @pytest.mark.asyncio
    async def test_process_batch_handles_exceptions(self, tmp_path):
        """Test process_batch handles exceptions gracefully."""
        raw_dir = tmp_path / "raw_images"
        display_dir = tmp_path / "display_images"
        failed_dir = tmp_path / "failed_images"
        raw_dir.mkdir()
        display_dir.mkdir()
        failed_dir.mkdir()

        # Create mix of valid and invalid images
        valid_file = raw_dir / "valid.jpg"
        valid_image = Image.new('RGB', (50, 50), color='green')
        valid_image.save(valid_file, format='JPEG')

        invalid_file = raw_dir / "invalid.jpg"
        invalid_file.write_bytes(b"Not valid")

        with patch('core.processor.RAW_IMAGES_DIR', raw_dir):
            with patch('core.processor.DISPLAY_IMAGES_DIR', display_dir):
                with patch('core.processor.FAILED_IMAGES_DIR', failed_dir):
                    results = await process_batch([valid_file, invalid_file])

                    # Should have 2 results
                    assert len(results) == 2
                    # Valid should succeed, invalid should fail
                    assert results[0] is True
                    assert results[1] is False
