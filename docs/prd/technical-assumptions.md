# Technical Assumptions

## Repository Structure: Monorepo

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

## Service Architecture: Monolith within Monorepo

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

**Backend:**
- **Language:** Python 3.10+ (mature, excellent file I/O libraries, systemd integration)
- **Web Framework:** FastAPI (async support for concurrent uploads, automatic OpenAPI docs, modern)
  - *Alternative:* Flask (simpler, more mature, synchronous—acceptable if async not critical)
- **Image Processing:** Pillow (PIL fork) for EXIF orientation, resizing, format validation
- **File Monitoring:** Watchdog library or simple polling loop (10-second interval per Brief)

**Frontend (Upload UI & Carousel):**
- **Framework:** Vanilla JavaScript + modern CSS (or lightweight React/Vue if justified)
  - *Rationale:* Minimal bundle size for fast mobile loading, no build complexity if possible
  - *Alternative:* React if UI state management becomes complex (optimistic uploads, retry logic)
- **Styling:** Tailwind CSS or simple custom CSS (prioritize small payload size)
- **Image Upload:** HTML5 File API, Fetch API for multipart form upload

**Infrastructure:**
- **Web Server:** Uvicorn (for FastAPI) or Nginx reverse proxy if needed
- **Process Manager:** systemd service with auto-restart on failure
- **Wi-Fi/Networking:** hostapd (access point daemon), dnsmasq (DHCP/DNS)
- **Storage:** ext4 filesystem on USB 3.0 SSD (500GB, faster than SD card)

## Testing Requirements: Unit + Integration + Manual Testing Convenience

**Decision:** Balanced testing pyramid focused on reliability and fast iteration

**Rationale:**
- **High reliability requirement:** 98% uptime target (NFR2) demands automated testing to catch regressions
- **MVP timeline constraint:** Don't over-invest in E2E complexity, but cover critical paths
- **Embedded system challenges:** Hardware-dependent features (Wi-Fi, HDMI output) need manual validation

**Testing Strategy:**

**1. Unit Tests (pytest):**
- Image processing logic (EXIF rotation, file validation, UUID generation)
- API endpoint logic (upload validation, error handling)
- File system operations (moving files, directory scanning)
- **Target:** 70%+ code coverage on business logic

**2. Integration Tests:**
- Full upload flow: POST multipart/form-data → file saved → processing triggered → carousel update
- Carousel state transitions: no photos → first photo → multiple photos
- Error scenarios: invalid file format, oversized uploads, disk full
- **Target:** Cover all critical user paths

**3. Manual Testing Conveniences:**
- **Mock photo generator script:** Creates dummy images for testing without real devices
- **Network simulation mode:** Run system on laptop Wi-Fi for development without Pi hardware
- **Carousel test page:** Allows manual triggering of transitions and state changes
- **Load testing script:** Simulate multiple concurrent uploads to validate 20-connection target

**4. Hardware Validation (Manual):**
- Real Raspberry Pi deployment testing (boot time, Wi-Fi range, HDMI output)
- Multi-device testing (iOS Safari, Android Chrome, older devices)
- Stress testing (100+ photos, 6-hour runtime, power cycle recovery)

**NOT in MVP scope:**
- ❌ Full E2E browser automation (Playwright/Selenium)—too slow for iteration speed
- ❌ Continuous performance benchmarking—manual validation sufficient for MVP
- ❌ Automated hardware-in-the-loop testing—requires expensive test rig

## Additional Technical Assumptions and Requests

**Deployment & Operations:**
- **Operating System:** Raspberry Pi OS Lite (64-bit, Debian-based, headless optimized)
- **Automated Provisioning:** Ansible playbook or shell script for reproducible Pi setup from fresh OS install
- **Configuration Management:** Environment variables or simple config file (YAML/JSON) for per-event customization (SSID, event name)
- **Logging:** Structured logging to local file for debugging (Python logging module), log rotation to prevent disk fill
- **Monitoring:** Systemd status checks sufficient for MVP (no external monitoring services—offline requirement)

**Security Assumptions:**
- **No authentication required:** Trade-off for zero-friction—acceptable for closed network event environment
- **Network isolation:** Device creates isolated Wi-Fi network, no internet gateway routing
- **Physical security:** Device is physically controlled by venue staff, not left in public unsecured locations
- **No HTTPS in MVP:** Local network HTTP acceptable; HTTPS adds certificate complexity without strong benefit for offline isolated network

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
