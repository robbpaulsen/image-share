# Image-Share Product Requirements Document (PRD)

**Version:** v1.0
**Last Updated:** 2025-10-13
**Status:** Draft

---

## Goals and Background Context

### Goals

- Deliver a zero-friction, offline photo aggregation system that transforms passive event photography into active guest entertainment
- Enable event venues to differentiate their offerings and justify premium pricing through unique technology features
- Eliminate venue staff burden through fully automated, plug-and-play operation requiring no technical expertise
- Provide comprehensive memory capture for event hosts by aggregating photos from all guest perspectives
- Establish product-market fit with casual event venues and planners within 3-6 months
- Build commercial credibility and track record to enable expansion into corporate event and memorial service markets

### Background Context

Image-Share addresses a fundamental gap in the event industry: guests capture hundreds of photos at social gatherings, but these remain isolated on individual devices, providing no real-time entertainment value and creating fragmented memories for hosts. Existing solutions fail due to internet dependency, high costs, or poor adoption from app-required platforms. Meanwhile, event venues struggle with commoditization, competing primarily on price in the absence of unique differentiators.

The solution leverages commercially-viable Raspberry Pi hardware to create a self-contained, offline photo display system. Guests connect to a dedicated Wi-Fi network, upload photos via browser (no app required), and see them appear on a central display within seconds. This transforms photography from passive documentation into active participation, creates ambient entertainment throughout events, and gives venues a marketable premium feature. The B2B channel model targets venues and professional event planners who benefit from operational efficiency and differentiation, while ultimately serving event hosts seeking comprehensive memory preservation and guest engagement.

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2025-10-13 | v1.0 | Initial PRD creation from Project Brief | John (PM Agent) |

---

## Requirements

### Functional

1. **FR1:** The system shall create a dedicated Wi-Fi access point with a configurable SSID that supports up to 20 concurrent client connections.
2. **FR2:** The system shall provide a browser-based upload interface accessible via a simple URL (e.g., `photoshare.local` or static IP `10.0.17.1`) requiring no app installation or user authentication.
3. **FR3:** The system shall accept photo uploads in common formats (JPEG, PNG, HEIC) up to 25MB per file via mobile web browsers.
4. **FR4:** The system shall automatically process uploaded photos by renaming them with UUIDs and moving them to the display directory.
5. **FR5:** The system shall display uploaded photos on a connected HDMI display in a chronological carousel format with a 7-second interval per photo.
6. **FR6:** The carousel shall automatically detect new photos and dynamically update without requiring manual refresh.
7. **FR7:** When no photos exist, the system shall display an instruction page with a QR code for Wi-Fi/URL access.
8. **FR8:** The system shall boot automatically on power connection and become fully operational within 3 minutes.
9. **FR9:** The system shall store all uploaded photos persistently on local storage.
10. **FR10:** The system shall provide a manual photo extraction mechanism for post-event delivery.
11. **FR11:** The upload interface shall provide immediate visual feedback confirming successful upload.

### Non-Functional

1. **NFR1:** Photo processing pipeline shall achieve 95th percentile latency of ≤15 seconds from upload completion to carousel display appearance.
2. **NFR2:** The system shall maintain 98% uptime during events.
3. **NFR3:** The Wi-Fi network shall support 20 concurrent connections with <5% connection failure rate.
4. **NFR4:** The upload interface shall be fully responsive and usable on smartphone screens (320px minimum width).
5. **NFR5:** The carousel display shall support resolutions up to 4K (3840×2160).
6. **NFR6:** System boot and initialization shall complete within 3 minutes from power-on.
7. **NFR7:** All data shall remain on the local device with zero external network communication (offline-first architecture).
8. **NFR8:** The hardware platform shall be a Raspberry Pi 4B (8GB RAM minimum) with 500GB storage and a ruggedized enclosure.
9. **NFR9:** The system shall operate reliably in typical venue environments (15-30°C).
10. **NFR10:** Upload interface load time shall be <3 seconds on the local network connection.
11. **NFR11:** The system shall implement automatic restart via systemd service management if core processes crash.
12. **NFR12:** Code and configuration shall be documented sufficiently for a technical handoff.

---

## User Interface Design Goals

### Overall UX Vision

The Image-Share interface embodies **radical simplicity** - eliminating every possible point of friction between "guest arrives at event" and "guest's photo appears on screen." The design philosophy is **invisible technology**: guests should feel like they're simply sharing to a "magic screen," not interacting with a technical system.

**Two distinct user experiences must coexist:**

1. **Guest Upload Interface (Mobile):** Brutally minimal, optimized for one-handed smartphone use in chaotic social environments (dim lighting, distraction, holding drinks). Large touch targets, minimal text, instant feedback.

2. **Carousel Display (Large Screen):** Ambient, elegant, and celebratory. Photos are the hero—UI chrome is minimal or absent. Design evokes "living memory wall" rather than "slideshow presentation."

**Assumption:** No venue/staff admin interface is in MVP scope—configuration happens via file/SSH pre-event.

### Key Interaction Paradigms

**Mobile Upload Experience:**
- **Progressive Web App (PWA) principles** without formal PWA installation—works like native app from browser
- **Single-purpose interaction model:** Landing page immediately presents "Upload Photo" as primary CTA
- **Optimistic UI:** Show upload success immediately, don't wait for backend confirmation (assume success, handle failures gracefully)
- **Ambient awareness:** If possible, show small "X photos in carousel" counter to create social proof

**Carousel Display Experience:**
- **Zero-interaction design:** Display never requires touch, mouse, or remote control input
- **Graceful photo transitions:** Smooth crossfade or slide transitions (not jarring cuts) with 7-second hold time
- **Contextual states:** Display adapts based on system state (no photos yet vs. active carousel vs. error states)
- **Unattended operation:** Can run for 6+ hours without intervention, degradation, or visual artifacts

**Assumption:** No gesture controls, voice commands, or interactive display features in MVP—pure passive viewing.

### Core Screens and Views

**Mobile Interface:**
1. **Landing/Upload Page** - Primary screen with upload CTA, connection instructions if needed, visual feedback on upload status
2. **Upload Confirmation** - Brief success state showing estimated time to display appearance
3. **Error/Retry Page** - Handles upload failures, file size issues, unsupported formats (edge case, but needs design)

**Display Interface:**
1. **Instruction Screen (No Photos State)** - QR code, Wi-Fi SSID, URL, visual instructions for first-time guests
2. **Carousel Screen (Active State)** - Full-screen photo display with minimal/no UI chrome, smooth transitions
3. **System Status Screen (Error State)** - Visible but non-alarming error message if system encounters issues (e.g., "Waiting for photos to process...")

**Assumption:** No admin/configuration screens for venue staff—this is handled outside the UI.

### Accessibility: WCAG AA

**Target Level:** WCAG 2.1 Level AA compliance for upload interface

**Rationale:**
- Event guests include users with diverse accessibility needs (visual impairments, motor challenges, cognitive differences)
- Level AA is industry standard for public-facing web applications and achievable without architectural complexity
- Primary interaction (photo upload) is inherently visual, but supporting features (text labels, keyboard navigation, sufficient contrast) must be accessible

**Specific Considerations:**
- Large touch targets (minimum 44×44px per WCAG guidelines) for upload buttons
- Sufficient color contrast for text and UI elements (4.5:1 minimum)
- Screen reader support for upload flow (semantic HTML, ARIA labels where needed)
- Keyboard navigation support for guests using alternative input devices

**Assumption:** Carousel display accessibility is not prioritized (it's ambient/passive viewing, not interactive). Focus accessibility investment on upload interface.

### Branding

**Visual Style:** Clean, modern, celebratory—evokes "event photography" without being overly formal

**Color Palette:**
- **Primary:** Warm, inviting tones (soft blues, friendly greens) that feel celebratory without being garish
- **Assumption:** No existing brand guidelines—need to establish Image-Share brand identity or make it white-label/customizable per venue

**Typography:**
- Clean, highly legible sans-serif (system fonts: -apple-system, Roboto) for zero load time and maximum compatibility
- Large font sizes for mobile (18px+ for body text) to ensure readability in varied lighting

**Tone:**
- Friendly and encouraging: "Share your photos!" not "Upload files"
- Casual, not corporate: "Your photo is on the way!" not "Upload successful"

**Logo/Branding Placement:**
- **Assumption:** Minimal Image-Share branding on interfaces—venues may want to co-brand or white-label
- QR code and instruction screen could include venue's custom logo or event name

**Open Question:** Should this be white-label (venues can customize branding) or branded as "Image-Share powered"? This affects marketing strategy.

### Target Device and Platforms: Web Responsive

**Primary Target:** Mobile web browsers (iOS Safari, Android Chrome)
- Smartphone-optimized responsive design (320px - 428px widths)
- Touch-first interaction model
- Progressive enhancement for older devices

**Secondary Target:** Desktop/tablet browsers (for testing, edge cases where guests use laptops)
- Upload interface scales to larger screens but maintains mobile-first design patterns

**Display Output:** Desktop browsers in kiosk mode (Chromium on Raspberry Pi)
- Full-screen carousel on HDMI-connected displays
- Supports resolutions up to 4K, optimized for common formats (1920×1080, 3840×2160)

**Assumption:** No native mobile apps (iOS/Android) in scope—PWA via browser only. This avoids app store friction and development complexity.

---

## Technical Assumptions

### Networking Environment Prerequisite (Out of Application Scope)

**Decision:** The Image-Share application relies on a pre-configured operating system that provides all necessary networking functionality. The development scope of the application **does not** include implementing this network infrastructure.

**Rationale:**
- This separates application development from platform administration, allowing developers to focus on user-facing features.
- The underlying OS of the Raspberry Pi is optimized to provide these services reliably.

**Environment Details:**
- The device operates as a **Wi-Fi Access Point (Router)**, creating its own isolated network.
- It runs **DHCP and DNS services** (`dnsmasq`) to assign IP addresses and resolve a local hostname (e.g., `photoshare.local`).
- The device has a **static IP address** on this network (e.g., `10.0.17.1`), which acts as the gateway and the address for the web service.

### Repository Structure: Monorepo

**Decision:** Single monorepo containing all system components (backend services, upload UI, carousel display UI, deployment scripts, documentation)

**Rationale:**
- **Simplicity:** Entire system fits on single device—no need for distributed repository complexity
- **Deployment atomicity:** Single Git clone deploys complete system to Raspberry Pi
- **Version coherence:** UI and backend changes stay synchronized (no cross-repo dependency hell)
- **Small team velocity:** Easier for solo/small team to manage one codebase vs. coordinating multiple repos
- **Aligns with MVP scope:** This is a self-contained appliance, not a distributed system

**Structure:**
```
/image-share
  /backend          # API server, image processing
  /upload-ui        # Mobile upload interface
  /carousel-ui      # Display interface
  /scripts          # Deployment, setup, photo extraction
  /docs             # Architecture, setup guides
  /tests            # Integration and unit tests
```

### Service Architecture: Monolith within Monorepo

**Decision:** Single backend process handling all server responsibilities (web server, API endpoints, image processing, file monitoring)

**Rationale:**
- **Resource constraints:** Raspberry Pi has limited CPU/RAM—avoid microservices overhead
- **Simplified deployment:** One service to start, monitor, and restart via systemd
- **Reduced complexity:** No inter-service communication, message queues, or orchestration needed
- **Adequate for scale:** 20 concurrent users is well within monolith capabilities
- **Faster iteration:** Changes don't require coordinating multiple service deployments

**NOT chosen alternatives:**
- ❌ **Microservices:** Over-engineering for this scale; adds network latency and failure points
- ❌ **Serverless:** Requires cloud infrastructure, violates offline-first principle

**Technology Stack Proposal:**

**Backend (Application Scope):**
- **Language:** Python 3.10+ (mature, excellent file I/O libraries)
- **Web Framework:** FastAPI (async support for concurrent uploads, automatic OpenAPI docs)
- **Image Processing:** Pillow (PIL fork) for image format validation.
- **File Monitoring:** Watchdog library or simple polling loop.

**Frontend (Application Scope):**
- **Framework:** Vanilla JavaScript + modern CSS.
  - *Rationale:* Minimal bundle size for fast mobile loading, no build complexity.
- **Styling:** Custom CSS to prioritize small payload size.
- **Image Upload:** HTML5 File API, Fetch API for multipart form upload.

**Infrastructure (Provided by Pre-configured OS Environment):**
- **Web Server:** Uvicorn (running the FastAPI app).
- **Process Manager:** systemd service with auto-restart on failure.
- **Wi-Fi/Networking:** hostapd (access point daemon), dnsmasq (DHCP/DNS).
- **Storage:** ext4 filesystem on USB 3.0 SSD (500GB, faster than SD card).

### Testing Requirements: Unit + Integration + Manual Testing Convenience

**Decision:** Balanced testing pyramid focused on reliability and fast iteration

**Rationale:**
- **High reliability requirement:** 98% uptime target (NFR2) demands automated testing to catch regressions.
- **MVP timeline constraint:** Don't over-invest in E2E complexity, but cover critical paths.
- **Embedded system challenges:** Hardware-dependent features (Wi-Fi, HDMI output) need manual validation as part of the platform.

**Testing Strategy:**

**1. Unit Tests (pytest for Application Scope):**
- Image processing logic (file validation, UUID generation).
- API endpoint logic (upload validation, error handling).
- File system operations (moving files, directory scanning).
- **Target:** 70%+ code coverage on business logic.

**2. Integration Tests (Application Scope):**
- Full upload flow: POST multipart/form-data → file saved → processing triggered → carousel update.
- Carousel state transitions: no photos → first photo → multiple photos.
- Error scenarios: invalid file format, oversized uploads, disk full.
- **Target:** Cover all critical user paths.

**3. Manual Testing Conveniences:**
- **Mock photo generator script:** Creates dummy images for testing without real devices.
- **Carousel test page:** Allows manual triggering of transitions and state changes.
- **Load testing script:** Simulate multiple concurrent uploads to validate connection targets.

**4. Hardware and Platform Validation (Manual):**
- Real Raspberry Pi deployment testing (boot time, Wi-Fi range and stability, HDMI output).
- Multi-device testing (iOS Safari, Android Chrome, older devices).
- Stress testing (100+ photos, 6-hour runtime, power cycle recovery).

**NOT in MVP scope:**
- ❌ Full E2E browser automation (Playwright/Selenium)—too slow for iteration speed.
- ❌ Continuous performance benchmarking—manual validation sufficient for MVP.
- ❌ Automated hardware-in-the-loop testing—requires expensive test rig.

### Additional Technical Assumptions and Requests

**Deployment & Operations:**
- **Operating System:** Raspberry Pi OS Lite (64-bit, Debian-based), pre-configured with networking services.
- **Automated Provisioning:** An Ansible playbook or shell script is used to deploy the *application* onto the pre-configured OS.
- **Configuration Management:** Environment variables or a simple config file (YAML/JSON) for per-event customization (e.g., event name).
- **Logging:** Structured logging to a local file for debugging (Python logging module), with log rotation.
- **Monitoring:** Systemd status checks are sufficient for MVP.

**Security Assumptions:**
- **No authentication required:** This is a trade-off for a zero-friction guest experience on the closed, private network created by the device.
- **Network isolation:** The device creates an isolated Wi-Fi network with no internet gateway routing. This is a key security feature of the platform.
- **Physical security:** The device is physically controlled by venue staff.
- **No HTTPS in MVP:** On the isolated local network, HTTP is acceptable.

**Photo Storage & Delivery:**
- **File Naming:** UUIDs prevent collisions, preserve upload order via timestamps in metadata or DB
- **No Database in MVP:** Filesystem-based photo management (directories as state) avoids DB dependency
  - *Reconsider if:* Need to track uploader metadata, implement moderation queues, or store event analytics
- **Post-Event Extraction:** Shell script that creates `event-photos-[date].zip` or copies to USB drive
- **No Automatic Deletion:** Photos persist until manual cleanup—venue staff responsible for wiping between events

**Future Extensibility Hooks (Not MVP, but Architect Should Consider):**
- **Moderation Interface:** Possible future need for staff to preview/approve photos before display (corporate events)
- **Photo Metadata:** May eventually want to track upload timestamp, device type, event association
- **Multi-Event Support:** Currently assumes one event per device wipe—could support multiple events with sessions/folders
- **Remote Management:** Future premium feature could allow cloud-based monitoring/configuration for venue chains

**Technology NOT Chosen (Explicit Rejections):**
- ❌ **Docker/Containers:** Adds complexity on embedded platform, systemd sufficient for process isolation
- ❌ **Node.js Backend:** Python preferred for stronger image processing ecosystem and DevOps simplicity
- ❌ **WebSockets for Real-Time Updates:** Polling adequate for 10-second update interval, reduces complexity
- ❌ **Object Storage (MinIO, etc.):** Filesystem sufficient for MVP scale

---

## Epic List

### Epic 1: Foundation & Photo Upload System
**Goal:** Establish project infrastructure, networking foundation, and working photo upload capability. Deploy to Raspberry Pi and demonstrate first photo upload and storage.

### Epic 2: Display Carousel & Real-Time Integration
**Goal:** Build the carousel display interface with automatic photo detection and create the complete upload-to-display pipeline. Demonstrate real-time photo appearance on screen after upload.

### Epic 3: Production Readiness & Deployment Automation
**Goal:** Harden system for reliable venue deployment with error handling, instruction screens, photo extraction tools, and automated provisioning. Prepare for pilot partnerships.

---

## Epic 1: Foundation & Photo Upload System

**Expanded Goal:** Establish the complete project foundation including monorepo structure and development environment. Implement a functional photo upload system where event guests can access a mobile-optimized web interface and successfully upload photos that are processed and stored. By epic completion, the system should boot automatically and accept photo uploads, with processed files ready for display integration in Epic 2.

---

### Story 1.1: Project Foundation and Development Environment

**As a** developer,
**I want** a properly structured monorepo with an initialized backend framework and basic web server,
**so that** I have a solid foundation for building features and can validate the development environment works.

#### Acceptance Criteria

1. Monorepo directory structure created with `/backend`, `/upload-ui`, `/carousel-ui`, `/scripts`, `/docs`, `/tests` folders.
2. Python 3.10+ virtual environment configured with FastAPI and Uvicorn dependencies.
3. Basic FastAPI application with a GET `/health` endpoint returning `{"status": "ok", "timestamp": <ISO8601>}`.
4. Health endpoint is accessible at `http://localhost:8000/health` and returns a 200 status code.
5. README.md documents development setup steps (venv creation, dependency installation, running the server).
6. `.gitignore` is configured to exclude `venv/`, `__pycache__/`, `.env`, and image directories.
7. Basic pytest setup exists with one passing test that validates the health endpoint response structure.

---

### Story 1.2: Photo Upload API Endpoint with Validation

**As a** event guest,
**I want** the backend to accept my photo uploads and validate them properly,
**so that** my valid photos are stored successfully and I receive clear feedback for invalid uploads.

#### Acceptance Criteria

1. A POST `/api/upload` endpoint accepts multipart/form-data with a `photo` field.
2. The endpoint validates the file format, accepting JPEG (.jpg, .jpeg), PNG (.png), and HEIC (.heic) formats.
3. The endpoint validates file size, rejecting files larger than 25MB with a 413 status and an error message `{"error": "File too large", "max_size_mb": 25}`.
4. Valid uploads are saved to an initial `raw_images/` directory.
5. A successful upload returns a 200 status with JSON: `{"success": true, "message": "Photo uploaded successfully"}`.
6. An invalid format returns a 400 status with an error message: `{"error": "Invalid file format", "accepted_formats": ["jpeg", "png", "heic"]}`.
7. The `raw_images/` directory is created automatically if it doesn't exist on server startup.
8. Unit tests cover: valid upload success, oversized file rejection, invalid format rejection, and missing file field handling.
9. Logging captures: upload timestamp, original filename, file size, and validation result (success/failure reason).

---

### Story 1.3: Mobile-Optimized Upload Interface

**As a** event guest,
**I want** a simple, fast-loading mobile web interface to upload my photos,
**so that** I can quickly share my event photos without confusion or technical difficulty.

#### Acceptance Criteria

1. An HTML upload page is accessible at the root path (`/`).
2. The page loads in <3 seconds on a local network (minimal CSS/JS, no external dependencies/CDNs).
3. The page is fully responsive on smartphone screens (320px - 428px widths) and tested on iOS Safari and Android Chrome.
4. The primary UI element is a large "Upload Photo" button (minimum 44x44px touch target per WCAG).
5. The button click opens the native device photo picker (using `<input type="file" accept="image/*">`).
6. After photo selection, a "Submit" or "Upload" button becomes active.
7. During upload, a visual loading indicator is displayed (e.g., a spinner).
8. On success, a confirmation message displays: "Photo uploaded! It will appear on the display soon." with an option to upload another.
9. On error (network, server error, invalid file), a clear error message is displayed with a retry option.
10. The page uses semantic HTML and sufficient color contrast (4.5:1 minimum) for WCAG AA compliance.

---

### Story 1.4: Photo Processing and File Movement

**As a** system operator,
**I want** uploaded photos to be renamed with a unique ID and moved to the final display directory,
**so that** they are ready to be served by the display endpoint without complex processing.

#### Acceptance Criteria

1. A background process monitors the initial upload directory for new files.
2. Each new image file is renamed to a unique UUID v4, preserving the original file extension (e.g., `a3f2b8c1-9d4e-4f6a-8c2b-1e3d5f7a9b0c.jpg`).
3. The renamed file is moved from its original directory to the final `display_images/` directory.
4. The original file from the upload directory is deleted after the move is successfully completed.
5. If the renaming or moving process fails, the original file is moved to a `failed_images/` directory and the error is logged.
6. The process ensures that file modification timestamps in the `display_images/` directory reflect the upload order for chronological sorting by the carousel.
7. Logging captures the mapping from the original filename to its new UUID filename, the processing timestamp, and any errors.
8. Unit tests are updated to cover UUID generation, file movement, and error handling for the move operation.

---

### Story 1.5: Systemd Service Configuration and Automated Startup

**As a** venue staff member,
**I want** the system to start automatically when I plug in the device,
**so that** I don't need technical knowledge or manual intervention to get it operational.

#### Acceptance Criteria

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

## Epic 2: Display Carousel & Real-Time Integration

**Expanded Goal:** Build a carousel display interface that automatically detects new photos in the `display_images/` directory and shows them in a continuous loop on the connected HDMI display. Implement smooth transitions, proper image scaling for various display resolutions, and state management to handle "no photos yet" scenarios. Complete the end-to-end pipeline from upload to display, validating the 10-15 second latency target and demonstrating the core product value: guests see their photos on screen shortly after upload.

---

### Story 2.1: Basic Carousel Display Interface and Photo Rendering

**As a** event attendee,
**I want** to see uploaded photos displayed on the venue screen in a continuous loop,
**so that** I can view all shared event moments and see my contributions appear publicly.

#### Acceptance Criteria

1. HTML carousel page accessible at `http://10.0.17.1/display` served by backend
2. Page displays full-screen photo view with no visible browser chrome (designed for kiosk mode)
3. Page loads all images from `display_images/` directory via API endpoint GET `/api/photos` returning JSON array of photo filenames
4. Photos are displayed one at a time, centered and scaled to fit display dimensions while preserving aspect ratio (no stretching or cropping)
5. Carousel supports display resolutions up to 4K (3840×2160); tested at common resolutions (1920×1080, 2560×1440, 3840×2160)
6. Portrait and landscape photos both display correctly with proper orientation
7. Black background fills any space around photos that don't fill the entire screen
8. Initial load shows first photo in chronological order (oldest uploaded photo based on file modification timestamp)
9. Page includes minimal/no visible UI chrome (no navigation buttons, filename displays, or other distractions in MVP)
10. CSS ensures images use `object-fit: contain` for proper scaling without distortion
11. Manual testing validates display on actual HDMI-connected monitor/TV, not just browser window

---

### Story 2.2: Automatic Carousel Rotation with 7-Second Intervals

**As a** event attendee,
**I want** the carousel to automatically advance through photos at regular intervals,
**so that** I can see all shared photos without manual interaction and the display provides continuous entertainment.

#### Acceptance Criteria

1. Carousel automatically advances to the next photo after 7 seconds (configurable via constant/environment variable)
2. Photos are shown in chronological order based on file modification timestamp (oldest first, ensuring fairness)
3. After displaying the last photo, carousel loops back to the first photo and continues indefinitely
4. Transition between photos uses smooth crossfade effect (1-second fade duration) to avoid jarring cuts
5. CSS transitions or JavaScript animation provides the crossfade (avoid heavy libraries if possible)
6. Carousel continues running without manual intervention or user interaction for at least 6 hours (tested in long-running scenario)
7. No memory leaks: browser memory usage remains stable during extended operation (monitor DevTools memory profiler over 30+ minute test)
8. If only one photo exists, it remains displayed continuously (no unnecessary transitions)
9. Carousel timing is consistent and doesn't drift over time (verify with stopwatch test over 20+ transitions)
10. Manual testing includes: single photo scenario, 2-photo scenario, 50+ photo scenario to validate all edge cases

---

### Story 2.3: Dynamic Photo Detection and Carousel Updates

**As a** event guest,
**I want** my newly uploaded photo to appear in the carousel without refreshing the display,
**so that** I see immediate feedback that my contribution was successful and is being shared with all attendees.

#### Acceptance Criteria

1. Carousel JavaScript polls GET `/api/photos` endpoint every 10 seconds to check for new photos
2. API endpoint returns list of photo filenames with file modification timestamps
3. Client-side logic detects changes by comparing current photo list to newly fetched list (identify new additions)
4. When new photos are detected, carousel dynamically adds them to the rotation queue without interrupting current display
5. New photos are inserted in chronological order; if carousel is mid-rotation, new photos appear after current loop completes (or intelligently inserted based on timestamp)
6. Hash comparison or timestamp comparison ensures carousel only updates when actual changes occur (avoids unnecessary DOM updates)
7. If carousel is showing "no photos" state (from Story 2.4), detecting first photo triggers automatic transition to carousel mode
8. Console logging shows: "Detected X new photos" with filenames when updates occur (for debugging)
9. End-to-end test: Upload photo via mobile interface → Verify photo appears in carousel within 20 seconds (10s processing + 10s polling + transition time)
10. Test validates behavior when multiple photos are uploaded simultaneously (batch detection works correctly)

---

### Story 2.4: No Photos State with Instruction Display

**As a** first arriving event guest,
**I want** to see clear instructions on how to upload photos when none exist yet,
**so that** I understand how to participate without needing venue staff assistance.

#### Acceptance Criteria

1. When `display_images/` directory is empty, carousel displays instruction screen instead of photo rotation
2. Instruction screen shows:
   - Large, clear heading: "Share Your Event Photos!"
   - Wi-Fi Network: The name of the event's Wi-Fi network (e.g., "ImageShare-Demo").
   - Upload URL: A simple URL like "photoshare.local" or the device's IP.
   - A QR code encoding the direct upload URL for quick smartphone access.
3. QR code is generated server-side or client-side and is scannable with smartphone camera apps (iOS/Android tested)
4. Instruction text is large, high-contrast (white text on dark background or equivalent) and readable from 10+ feet away
5. Screen uses friendly, welcoming tone matching branding guidelines from Section 3 (casual, encouraging)
6. When first photo is processed and detected (via polling from Story 2.3), display automatically transitions from instruction screen to carousel mode
7. Transition is smooth (crossfade, not jarring cut) and takes ~1 second
8. If all photos are manually deleted while carousel is running, display reverts to instruction screen within 10 seconds (next polling cycle)
9. QR code library used is lightweight (qrcode.js or server-side generation with Pillow) to minimize page load time
10. Manual test: Fresh system with no photos → Display shows instructions → Upload first photo → Display transitions to carousel automatically

---

### Story 2.5: End-to-End Upload-to-Display Integration Testing

**As a** product developer,
**I want** comprehensive integration tests validating the complete upload-to-display pipeline,
**so that** I can confidently deploy to pilot venues knowing the core user experience works reliably.

#### Acceptance Criteria

1. Integration test suite covers complete flow: mobile upload → API processing → file system → carousel detection → display
2. Test: Upload single photo, verify it appears in carousel within 20 seconds (automated or manual timing validation)
3. Test: Upload 5 photos in quick succession, verify all appear in chronological order in carousel
5. Test: Measure upload-to-display latency (P50, P95 percentiles) over 20 upload samples; confirm P95 ≤ 15 seconds (NFR1)
6. Test: Concurrent uploads from multiple devices (simulate 5 simultaneous uploads), verify all photos process correctly without corruption
7. Test: Error scenario - upload invalid file format, verify API rejects it and carousel is unaffected
8. Test: Network stability - verify system handles client disconnection/reconnection during upload gracefully
9. Test: Long-running stability - system runs for 2+ hours with periodic uploads (every 5 minutes), no crashes or memory leaks
10. Load test script simulates 20 concurrent connections uploading photos; measure system responsiveness and success rate
11. Documentation captures test procedures, results, and any identified performance bottlenecks or limitations
12. Test results inform any necessary optimizations before Epic 3 production hardening

---

### Story 2.6: Display Page Browser Kiosk Mode Configuration

**As a** venue staff member,
**I want** the display page to launch automatically in fullscreen kiosk mode on Raspberry Pi boot,
**so that** attendees see only the carousel without browser UI, tabs, or navigation elements.

#### Acceptance Criteria

1. Chromium browser configured to launch on Raspberry Pi boot in kiosk mode (`--kiosk` flag)
2. Browser opens directly to `http://localhost:8000/display` (or 10.0.17.1/display)
3. Kiosk mode provides true fullscreen: no address bar, tabs, bookmarks, or browser chrome visible
4. Mouse cursor is hidden after 3 seconds of inactivity (or permanently hidden via config)
5. Keyboard shortcuts for exiting fullscreen (F11, Ctrl+W, etc.) are disabled or intercepted
6. Screen blanking/screensaver is disabled (display remains active continuously)
7. Raspberry Pi desktop environment is minimized or hidden (only Chromium window visible)
8. Configuration persists across reboots (autostart script in ~/.config/autostart/ or systemd user service)
9. Test: Cold boot Raspberry Pi with HDMI display connected → Within 3.5 minutes, carousel displays in fullscreen kiosk mode
10. Test: Leave system idle for 30 minutes → Screen remains active showing carousel, no screensaver or blanking occurs
11. Documentation includes: accessing the system for maintenance (SSH or how to exit kiosk mode), troubleshooting display issues

---

## Epic 3: Production Readiness & Deployment Automation

**Expanded Goal:** Harden the system for reliable operation in venue environments with comprehensive error handling, graceful degradation, and clear user feedback for all failure scenarios. Implement photo extraction tools for post-event delivery to hosts. Create automated provisioning scripts that allow reproducible Raspberry Pi setup from fresh OS installation. Prepare complete documentation for venue staff handoff. Validate system stability under stress conditions and prepare for pilot partnership deployments.

---

### Story 3.1: Comprehensive Error Handling and User Feedback

**As a** event guest,
**I want** clear, helpful error messages when something goes wrong,
**so that** I understand what happened and can retry or seek assistance without frustration.

#### Acceptance Criteria

1. **Upload Interface Error States:**
   - Network timeout during upload: "Upload interrupted. Please check your connection and try again."
   - Server error (500): "Something went wrong on our end. Please try again in a moment."
   - File too large: "This photo is too large (max 25MB). Try a smaller image."
   - Invalid format: "This file format isn't supported. Please upload JPEG, PNG, or HEIC images."
   - Disk full: "Storage is full. Please notify venue staff."
2. Error messages use friendly, non-technical language appropriate for general audience
3. Each error state includes a "Try Again" button that resets the upload form
4. Retry functionality clears previous error state and allows fresh upload attempt
5. **Carousel Display Error States:**
   - Backend unreachable: Display shows "System temporarily unavailable" message (not blank screen or browser error)
   - No photos but polling fails: Instruction screen remains visible, logs error quietly
   - Image fails to load (404/broken): Skip to next photo, log error, don't break carousel rotation
6. **Backend Logging:**
   - All errors logged with structured format: timestamp, error type, user-facing message, technical details, stack trace if applicable
   - Logs written to `/var/log/image-share/app.log` with rotation configured (max 100MB, keep 5 files)
7. Test all error scenarios manually: disconnect network mid-upload, kill backend during upload, fill disk to 100%, upload 30MB file, upload .txt file
8. Error handling doesn't crash or hang the system—graceful degradation in all scenarios
9. Errors don't expose sensitive system information (file paths, stack traces) to end users
10. HTTP status codes are semantically correct (400 for client errors, 500 for server errors, 413 for payload too large)

---

### Story 3.2: System Health Monitoring and Self-Recovery

**As a** venue staff member,
**I want** the system to detect and recover from failures automatically,
**so that** events aren't disrupted by temporary technical issues and I don't need to intervene.

#### Acceptance Criteria

1. Enhanced `/api/health` endpoint returns detailed status:
   ```json
   {
     "status": "healthy",
     "timestamp": "2025-10-13T14:32:00Z",
     "checks": {
       "disk_space": {"status": "ok", "free_gb": 450},
       "photo_processing": {"status": "ok", "queue_length": 2},
       "upload_api": {"status": "ok"}
     }
   }
   ```
2. Health check detects degraded states:
   - Disk space <10GB: status "warning", logs alert
   - Disk space <1GB: status "critical", stops accepting uploads, displays maintenance message
   - Photo processing queue >20 files: status "warning" (potential backlog)
3. Systemd service restart policy tested: Kill backend process (SIGKILL), verify automatic restart within 15 seconds
4. Background watchdog process monitors backend responsiveness (HTTP health check every 60 seconds)
5. If backend becomes unresponsive (health check fails 3 consecutive times), watchdog triggers systemd restart
6. Carousel page implements retry logic: If photo fetch fails, retry after 30 seconds (don't leave display broken)
7. Processing pipeline resilience: If photo processing fails on corrupted file, move to `failed_images/`, log error, continue processing queue
8. Test scenarios:
   - Fill disk to 98% → Verify system stops uploads gracefully, displays error to users
   - Upload 50 photos simultaneously → Verify all process eventually, system doesn't hang
   - Corrupt one image file manually → Verify processing skips it and continues with others
9. Logging captures all recovery actions: "Backend restarted due to health check failure", "Skipped corrupted file: abc123.jpg"
10. Documentation includes troubleshooting guide: "If display is frozen, check systemd status...", "If photos aren't appearing, check disk space..."

---

### Story 3.3: Post-Event Photo Extraction and Export Tool

**As a** venue staff member,
**I want** a simple tool to package all event photos for delivery to the event host,
**so that** I can provide comprehensive photo archives without manually copying files or understanding the file system.

#### Acceptance Criteria

1. Shell script created at `/opt/image-share/scripts/extract-photos.sh` (or similar path)
2. Script usage: `./extract-photos.sh [event-name]` creates zip file: `event-photos-[event-name]-[date].zip`
3. Zip file contains all photos from `display_images/` directory with sequential numbering:
   - Original: `a3f2b8c1-9d4e-4f6a-8c2b-1e3d5f7a9b0c.jpg`
   - In zip: `001.jpg`, `002.jpg`, ... (ordered chronologically by upload time)
4. Script creates zip file in `/home/pi/event-exports/` directory (or user-configurable output path)
5. Script includes metadata file in zip: `event-info.txt` containing:
   - Event name
   - Export date/time
   - Total photo count
   - Optional: Upload timestamp range (first photo to last photo)
6. Script provides progress feedback: "Packaging 247 photos... Done! Created: event-photos-birthday-2025-10-13.zip"
7. After successful export, script offers optional cleanup: "Delete source photos? (y/N)" to prepare for next event
8. If user confirms cleanup, script moves photos from `display_images/` to `archived/[event-name]/` (safe backup before deletion)
9. Script validates zip integrity after creation (test extract to temp directory)
10. Documentation for venue staff includes:
    - Step-by-step instructions with screenshots
    - How to access Raspberry Pi (SSH or connect keyboard/monitor)
    - How to transfer zip file to USB drive: `cp event-photos-*.zip /media/usb/`
    - Troubleshooting: "What if script says 'No photos found'?"
11. Manual test: Run script after simulated event with 50 photos → Verify zip contains all 50 in correct order with metadata

---

### Story 3.4: Automated Raspberry Pi Provisioning System

**As a** system deployer,
**I want** an automated provisioning script that configures a fresh Raspberry Pi from clean OS install to fully operational Image-Share device,
**so that** I can rapidly deploy multiple units for venue partnerships without manual configuration steps.

#### Acceptance Criteria

1. Provisioning solution implemented as Ansible playbook OR comprehensive shell script (Ansible preferred for idempotency)
2. Script/playbook starts from: Raspberry Pi OS Lite 64-bit, fresh install with SSH enabled and network configured
3. The provisioning script for the *application* performs the following tasks on a pre-configured base OS:
   - Install application dependencies: Python 3.10+, Chromium browser.
   - Create the application user and directory structure (`/opt/image-share/`, log directories, image directories).
   - Clone/copy the Image-Share application codebase from a git repository or local source.
   - Install Python dependencies into a virtual environment.
   - Install the application's systemd service files (backend service, kiosk autostart).
   - Enable the application services to start on boot.
4. Provisioning is idempotent: Running twice doesn't break anything or cause errors
5. Provisioning accepts configuration parameters:
   - Wi-Fi SSID (default: "ImageShare-Demo")
   - Event name or device identifier
   - Admin SSH key for secure access
6. Provisioning completes in <15 minutes on typical Raspberry Pi 4B with good SD card
7. After provisioning, reboot Raspberry Pi → System should boot into fully operational state within 3.5 minutes
8. Dry-run mode available: `--check` flag shows what would be changed without applying changes
9. Logging captures all provisioning steps and any errors encountered
10. Documentation includes:
    - Prerequisites: How to prepare fresh Raspberry Pi OS
    - How to run provisioning: `ansible-playbook provision.yml -i hosts --extra-vars "ssid=MyEvent"`
    - How to customize configuration variables
    - Rollback procedure if provisioning fails mid-way
11. Test: Provision two Raspberry Pis with different SSIDs → Both boot successfully and operate independently

---

### Story 3.5: Venue Staff Operations Guide and Troubleshooting Documentation

**As a** venue staff member with limited technical background,
**I want** clear, visual documentation covering setup, operation, and troubleshooting,
**so that** I can confidently deploy and manage the system without needing developer support.

#### Acceptance Criteria

1. **Quick Start Guide (docs/venue-quick-start.md):**
   - Step 1: "Plug device into power outlet" (photo of device and power connection)
   - Step 2: "Connect HDMI cable to display" (photo of HDMI connection)
   - Step 3: "Wait 3-4 minutes for system to boot" (what to expect on screen)
   - Step 4: "Verify display shows instructions or carousel"
   - Total length: 1-2 pages, heavily illustrated
2. **Operation Guide (docs/venue-operations.md):**
   - How to verify system is working (checklist: display active, Wi-Fi visible, upload test)
   - What normal operation looks like (display states, expected behavior)
   - When to intervene vs. when to leave it alone
   - How to monitor photo uploads during event (optional: check photo count via SSH or status page)
3. **Troubleshooting Guide (docs/venue-troubleshooting.md):**
   - Issue: "Display is blank" → Check HDMI connection, check power, reboot device
   - Issue: "Guests can't connect to Wi-Fi" → Verify SSID, check device is powered, check Wi-Fi enabled on guest phone
   - Issue: "Photos aren't appearing on display" → Check disk space, check backend service status
   - Issue: "System not responding" → Safe reboot procedure: unplug power, wait 10 seconds, plug back in
   - Each issue includes: symptoms, likely causes, step-by-step resolution, when to escalate
4. **Post-Event Guide (docs/post-event.md):**
   - How to extract photos: Step-by-step running extract-photos.sh script
   - How to transfer photos to USB drive
   - How to deliver photos to event host (naming convention, folder structure)
   - How to clean up for next event (optional photo deletion, archive management)
5. **All documentation:**
   - Written at 8th-grade reading level (simple language, short sentences)
   - Uses screenshots or photos where possible (actual Raspberry Pi hardware, actual screens)
   - Includes "call for help" contact info: who to reach if troubleshooting doesn't work
   - Available in both English and Spanish (per Mexico market requirements)
   - PDF and Markdown formats provided
6. Documentation tested with non-technical user: Give docs to someone unfamiliar with system, observe them following instructions, identify confusing areas
7. Docs stored in `/opt/image-share/docs/` on device and in git repository
8. Quick reference card (single laminated page) created for venue staff: most common tasks and troubleshooting steps

---

### Story 3.6: Production Stress Testing and Stability Validation

**As a** product owner,
**I want** comprehensive stress testing to validate system meets reliability targets under real-world conditions,
**so that** I can confidently deploy to pilot venues knowing the system won't fail during critical events.

#### Acceptance Criteria

1. **Long-Running Stability Test:**
   - System runs continuously for 8 hours with periodic photo uploads (every 2-5 minutes, randomized)
   - Test completes without crashes, memory leaks, or performance degradation
   - Memory usage remains stable (<2GB RAM, no upward trend)
   - Photo processing latency remains consistent (P95 ≤ 15 seconds throughout test)
2. **Concurrent Upload Load Test:**
   - Simulate 20 concurrent clients uploading photos simultaneously
   - All uploads succeed or fail gracefully (no server crashes, data corruption, or hung connections)
   - Success rate ≥95% under load
   - Measure: average upload time, P95 latency, error rate
3. **Network Resilience Test:**
   - Client disconnects mid-upload → Server handles gracefully, client can retry
   - Multiple clients rapidly connecting/disconnecting → Wi-Fi AP remains stable
   - 20 concurrent connections maintained simultaneously (NFR3 validation)
4. **Storage Limit Test:**
   - Upload photos until disk reaches 99% capacity
   - System stops accepting uploads gracefully, displays maintenance message
   - No crashes or data corruption when disk full
   - After freeing space, system resumes normal operation
5. **Error Recovery Test:**
   - Kill backend process during active uploads → Systemd restarts, system recovers
   - Corrupt image file in processing queue → System skips it, continues processing others
   - Power cycle Raspberry Pi mid-operation → System boots and resumes normal state
6. **Display Endurance Test:**
   - Carousel runs for 6+ hours continuously displaying 100+ photos
   - No visual glitches, frozen frames, or black screens
   - Kiosk mode remains active (no exit to desktop, no screensaver)
   - Browser memory usage remains stable
7. **Real-Device Testing:**
   - Test with 5+ different smartphones (mix of iOS and Android, old and new models)
   - Verify upload interface works on all devices
   - Verify Wi-Fi connection success rate across devices
   - Document any device-specific issues or limitations
8. **Temperature and Environmental Testing:**
   - Run system in warm environment (25-30°C) for 4+ hours → No thermal throttling or failures
   - Verify Raspberry Pi temperature remains within safe operating range (<80°C)
9. **Test Results Documented:**
   - Create test report summarizing all stress test results
   - Document any failures or issues discovered with resolutions
   - Confirm system meets or exceeds all NFRs (98% uptime, 15s latency, 20 connections)
   - Identify any edge cases or limitations for venue staff awareness
10. **Pilot Readiness Checklist:**
    - All critical bugs resolved (no show-stoppers)
    - Documentation complete and reviewed
    - Provisioning script successfully creates deployable devices
    - Test device available for demonstration to pilot partners

---

## Checklist Results Report

_This section will be populated after executing the PM checklist to validate PRD quality and completeness._

---

## Next Steps

### UX Expert Prompt

_To be generated after checklist completion._

### Architect Prompt

_To be generated after checklist completion._

---

**END OF DOCUMENT**
