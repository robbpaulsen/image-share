# Epic 1: Foundation & Photo Upload System

**Expanded Goal:** Establish the complete project foundation including monorepo structure, development environment, and Raspberry Pi network configuration. Implement a functional photo upload system where event guests can connect to the device's Wi-Fi network, access a mobile-optimized web interface, and successfully upload photos that are processed and stored. By epic completion, the system should boot automatically and accept photo uploads, with processed files ready for display integration in Epic 2.

---

## Scope and Assumptions

To ensure clarity and focus, the project's scope is defined by the following technical assumptions:

*   **Network Functionality (Out of Scope):** The application operates under the assumption that the underlying system (the Raspberry Pi) is pre-configured to function as a Wi-Fi Access Point. This includes providing a stable Wi-Fi network, DHCP for IP address assignment, and DNS resolution for a local domain (e.g., `photoshare.local`). The development of the application **does not** include implementing, configuring, or managing these network services (`hostapd`, `dnsmasq`, etc.). They are considered part of the execution environment.

*   **Image Processing (In Scope):** The application's responsibility for image processing is strictly limited to renaming and moving files. The process is:
    1.  Rename the uploaded image file to a unique UUID v4 identifier while preserving the original file extension.
    2.  Move the renamed file to the final `display_images` directory.
    *   Any other form of image manipulation, such as EXIF-based orientation correction, watermarking, or resizing, is **explicitly out of scope** for this development cycle.

---

---

## Story 1.1: Project Foundation and Development Environment

**As a** developer,
**I want** a properly structured monorepo with initialized backend framework and basic web server,
**so that** I have a solid foundation for building features and can validate the development environment works.

### Acceptance Criteria

1. Monorepo directory structure created with `/backend`, `/upload-ui`, `/carousel-ui`, `/scripts`, `/docs`, `/tests` folders
2. Python 3.10+ virtual environment configured with FastAPI, Uvicorn, and Pillow dependencies
3. Basic FastAPI application with GET `/health` endpoint returning `{"status": "ok", "timestamp": <ISO8601>}`
4. Health endpoint accessible at `http://localhost:8000/health` and returns 200 status code
5. README.md documents development setup steps (venv creation, dependency installation, running server)
6. `.gitignore` configured to exclude `venv/`, `__pycache__/`, `.env`, and image directories
7. Basic pytest setup with one passing test validating health endpoint response structure
8. Ensure the core image directories (`raw_images`, `display_images`, `failed_images`) are created on application startup if they do not exist.

---

## Story 1.3: Photo Upload API Endpoint with Validation

**As a** event guest,
**I want** the backend to accept my photo uploads and validate them properly,
**so that** my valid photos are stored successfully and I receive clear feedback for invalid uploads.

### Acceptance Criteria

1. POST `/api/upload` endpoint accepts multipart/form-data with `photo` field
2. Endpoint validates file format: accepts JPEG (.jpg, .jpeg), PNG (.png), HEIC (.heic) formats
3. Endpoint validates file size: rejects files larger than 25MB with 413 status and error message `{"error": "File too large", "max_size_mb": 25}`
4. Valid uploads are saved to `raw_images/` directory with temporary filename (original name preserved temporarily)
5. Successful upload returns 200 status with JSON: `{"success": true, "message": "Photo uploaded successfully", "filename": "<original_name>"}`
6. Invalid format returns 400 status with error message: `{"error": "Invalid file format", "accepted_formats": ["jpeg", "png", "heic"]}`
7. Duplicate simultaneous uploads do not cause file collisions (temporary filenames include timestamp or random suffix)
8. `raw_images/` directory is created automatically if it doesn't exist on server startup
9. Unit tests cover: valid upload success, oversized file rejection, invalid format rejection, missing file field handling
10. Logging captures: upload timestamp, original filename, file size, validation result (success/failure reason)

---

## Story 1.4: Mobile-Optimized Upload Interface

**As a** event guest,
**I want** a simple, fast-loading mobile web interface to upload my photos,
**so that** I can quickly share my event photos without confusion or technical difficulty.

### Acceptance Criteria

1. HTML upload page accessible at `http://10.0.17.1/` (root path) and `http://photoshare.local/` if DNS working
2. Page loads in <3 seconds on local network (minimal CSS/JS, no external dependencies/CDNs)
3. Page is fully responsive on smartphone screens (320px - 428px widths tested on iOS Safari and Android Chrome)
4. Primary UI element is large "Upload Photo" button (minimum 44x44px touch target per WCAG)
5. Button click opens native device photo picker (using `<input type="file" accept="image/*">`)
6. After photo selection, immediate visual feedback shows selected photo thumbnail preview
7. "Submit" / "Upload" button appears after photo selection (or auto-submits based on UX decision)
8. During upload, visual loading indicator displays (spinner or progress message)
9. On success, confirmation message displays: "Photo uploaded! It will appear on the display soon." with option to upload another
10. On error (network, server error, invalid file), clear error message displays with retry option
11. Page uses semantic HTML and sufficient color contrast (4.5:1 minimum) for WCAG AA compliance
12. No console errors on page load or during upload flow in browser developer tools
13. Testing validates flow on actual iOS (Safari) and Android (Chrome) devices, not just desktop emulation

---

## Story 1.5: Photo Processing and Storage

**As a** system operator,
**I want** uploaded photos to be automatically processed, renamed, and moved to the display directory,
**so that** photos are organized and ready for display without manual intervention.

### Acceptance Criteria

1. Background process monitors `raw_images/` directory every 10 seconds for new files.
2. Each new image file is processed by renaming it to a UUID v4 filename (e.g., `a3f2b8c1-9d4e-4f6a-8c2b-1e3d5f7a9b0c.jpg`), preserving the original file extension.
3. The processed (renamed) image is saved to the `display_images/` directory.
4. The original file in `raw_images/` is deleted after successful processing.
5. If processing fails (e.g., due to a corrupted image file), the file is moved to the `failed_images/` directory and an error is logged.
6. The processing logic handles up to 5 concurrent uploads queued without data loss or corruption.
7. The `display_images/` directory preserves chronological order via file modification timestamps.
8. Logging captures the original filename to UUID mapping, processing timestamp, and any errors encountered.
9. Unit tests cover UUID generation uniqueness, file move operations, and error handling for corrupted files.

---

## Story 1.6: Systemd Service Configuration and Automated Startup

**As a** venue staff member,
**I want** the system to start automatically when I plug in the device,
**so that** I don't need technical knowledge or manual intervention to get it operational.

### Acceptance Criteria

1. Systemd service file created at `/etc/systemd/system/image-share.service`
2. Service configured with 180-second (3-minute) delayed start (`ExecStartPre=/bin/sleep 180`) to allow network initialization
3. Service runs backend server (Uvicorn) as non-root user with appropriate permissions
4. Service configured for automatic restart on failure (`Restart=on-failure`, `RestartSec=10`)
5. Service enabled to start on boot (`systemctl enable image-share.service`)
6. Test: Cold boot of Raspberry Pi results in service running and accessible within 3.5 minutes of power-on
7. Test: Manually killing the backend process (`kill -9 <PID>`) results in automatic restart within 15 seconds
8. Service logs to journald; logs viewable with `journalctl -u image-share.service -f`
9. Health check script validates service is responding correctly (HTTP GET to `/health` returns 200)
10. Documentation includes: starting/stopping service manually, viewing logs, checking service status, troubleshooting startup failures

---
