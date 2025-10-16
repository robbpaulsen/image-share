# Epic 2: Display Carousel & Real-Time Integration

**Expanded Goal:** Build a carousel display interface that automatically detects new photos in the `display_images/` directory and shows them in a continuous loop on the connected HDMI display. Implement smooth transitions, proper image scaling for various display resolutions, and state management to handle "no photos yet" scenarios. Complete the end-to-end pipeline from upload to display, validating the 10-15 second latency target and demonstrating the core product value: guests see their photos on screen shortly after upload.

---

## Story 2.1: Basic Carousel Display Interface and Photo Rendering

**As a** event attendee,
**I want** to see uploaded photos displayed on the venue screen in a continuous loop,
**so that** I can view all shared event moments and see my contributions appear publicly.

### Acceptance Criteria

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

## Story 2.2: Automatic Carousel Rotation with 7-Second Intervals

**As a** event attendee,
**I want** the carousel to automatically advance through photos at regular intervals,
**so that** I can see all shared photos without manual interaction and the display provides continuous entertainment.

### Acceptance Criteria

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

## Story 2.3: Dynamic Photo Detection and Carousel Updates

**As a** event guest,
**I want** my newly uploaded photo to appear in the carousel without refreshing the display,
**so that** I see immediate feedback that my contribution was successful and is being shared with all attendees.

### Acceptance Criteria

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

## Story 2.4: No Photos State with Instruction Display

**As a** first arriving event guest,
**I want** to see clear instructions on how to upload photos when none exist yet,
**so that** I understand how to participate without needing venue staff assistance.

### Acceptance Criteria

1. When `display_images/` directory is empty, carousel displays instruction screen instead of photo rotation
2. Instruction screen shows:
   - Large, clear heading: "Share Your Event Photos!"
   - Wi-Fi network name: "Connect to: ImageShare-Demo"
   - Upload URL: "Open: http://photoshare.local or http://10.0.17.1"
   - QR code encoding the upload URL for quick smartphone access
3. QR code is generated server-side or client-side and is scannable with smartphone camera apps (iOS/Android tested)
4. Instruction text is large, high-contrast (white text on dark background or equivalent) and readable from 10+ feet away
5. Screen uses friendly, welcoming tone matching branding guidelines from Section 3 (casual, encouraging)
6. When first photo is processed and detected (via polling from Story 2.3), display automatically transitions from instruction screen to carousel mode
7. Transition is smooth (crossfade, not jarring cut) and takes ~1 second
8. If all photos are manually deleted while carousel is running, display reverts to instruction screen within 10 seconds (next polling cycle)
9. QR code library used is lightweight (qrcode.js or server-side generation with Pillow) to minimize page load time
10. Manual test: Fresh system with no photos → Display shows instructions → Upload first photo → Display transitions to carousel automatically

---

## Story 2.5: End-to-End Upload-to-Display Integration Testing

**As a** product developer,
**I want** comprehensive integration tests validating the complete upload-to-display pipeline,
**so that** I can confidently deploy to pilot venues knowing the core user experience works reliably.

### Acceptance Criteria

1. Integration test suite covers complete flow: mobile upload → API processing → file system → carousel detection → display
2. Test: Upload single photo, verify it appears in carousel within 20 seconds (automated or manual timing validation)
3. Test: Upload 5 photos in quick succession, verify all appear in chronological order in carousel
4. Test: Verify EXIF orientation correction end-to-end (upload rotated photo, confirm carousel displays it upright)
5. Test: Measure upload-to-display latency (P50, P95 percentiles) over 20 upload samples; confirm P95 ≤ 15 seconds (NFR1)
6. Test: Concurrent uploads from multiple devices (simulate 5 simultaneous uploads), verify all photos process correctly without corruption
7. Test: Error scenario - upload invalid file format, verify API rejects it and carousel is unaffected
8. Test: Network stability - verify system handles client disconnection/reconnection during upload gracefully
9. Test: Long-running stability - system runs for 2+ hours with periodic uploads (every 5 minutes), no crashes or memory leaks
10. Load test script simulates 20 concurrent connections uploading photos; measure system responsiveness and success rate
11. Documentation captures test procedures, results, and any identified performance bottlenecks or limitations
12. Test results inform any necessary optimizations before Epic 3 production hardening

---

## Story 2.6: Display Page Browser Kiosk Mode Configuration

**As a** venue staff member,
**I want** the display page to launch automatically in fullscreen kiosk mode on Raspberry Pi boot,
**so that** attendees see only the carousel without browser UI, tabs, or navigation elements.

### Acceptance Criteria

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
