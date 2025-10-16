# Epic 3: Production Readiness & Deployment Automation

**Expanded Goal:** Harden the system for reliable operation in venue environments with comprehensive error handling, graceful degradation, and clear user feedback for all failure scenarios. Implement photo extraction tools for post-event delivery to hosts. Create automated provisioning scripts that allow reproducible Raspberry Pi setup from fresh OS installation. Prepare complete documentation for venue staff handoff. Validate system stability under stress conditions and prepare for pilot partnership deployments.

---

## Story 3.1: Comprehensive Error Handling and User Feedback

**As a** event guest,
**I want** clear, helpful error messages when something goes wrong,
**so that** I understand what happened and can retry or seek assistance without frustration.

### Acceptance Criteria

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

## Story 3.2: System Health Monitoring and Self-Recovery

**As a** venue staff member,
**I want** the system to detect and recover from failures automatically,
**so that** events aren't disrupted by temporary technical issues and I don't need to intervene.

### Acceptance Criteria

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

## Story 3.3: Post-Event Photo Extraction and Export Tool

**As a** venue staff member,
**I want** a simple tool to package all event photos for delivery to the event host,
**so that** I can provide comprehensive photo archives without manually copying files or understanding the file system.

### Acceptance Criteria

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

## Story 3.4: Automated Raspberry Pi Provisioning System

**As a** system deployer,
**I want** an automated provisioning script that configures a fresh Raspberry Pi from clean OS install to fully operational Image-Share device,
**so that** I can rapidly deploy multiple units for venue partnerships without manual configuration steps.

### Acceptance Criteria

1. Provisioning solution implemented as Ansible playbook OR comprehensive shell script (Ansible preferred for idempotency)
2. Script/playbook starts from: Raspberry Pi OS Lite 64-bit, fresh install with SSH enabled and network configured
3. Provisioning performs all setup tasks:
   - Install system dependencies: Python 3.10+, hostapd, dnsmasq, Chromium browser
   - Create application user and directory structure (`/opt/image-share/`, log directories, image directories)
   - Clone/copy Image-Share codebase from git repository or local source
   - Install Python dependencies in virtual environment
   - Configure hostapd with customizable SSID (via variable/parameter)
   - Configure dnsmasq for DHCP and DNS
   - Configure static IP 10.0.17.1 on AP interface
   - Install systemd service files (backend service, kiosk autostart)
   - Enable services for boot startup
   - Disable screen blanking and power management
   - Configure log rotation
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

## Story 3.5: Venue Staff Operations Guide and Troubleshooting Documentation

**As a** venue staff member with limited technical background,
**I want** clear, visual documentation covering setup, operation, and troubleshooting,
**so that** I can confidently deploy and manage the system without needing developer support.

### Acceptance Criteria

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

## Story 3.6: Production Stress Testing and Stability Validation

**As a** product owner,
**I want** comprehensive stress testing to validate system meets reliability targets under real-world conditions,
**so that** I can confidently deploy to pilot venues knowing the system won't fail during critical events.

### Acceptance Criteria

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
