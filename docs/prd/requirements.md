# Requirements

## Functional

1. **FR1:** The system shall create a dedicated Wi-Fi access point with configurable SSID (default pattern: "PartyPhotos-[Event]") that supports up to 20 concurrent client connections
2. **FR2:** The system shall provide a browser-based upload interface accessible via simple URL (e.g., `photoshare.local` or static IP `10.0.17.1`) requiring no app installation or user authentication
3. **FR3:** The system shall accept photo uploads in common formats (JPEG, PNG, HEIC) up to 25MB per file via mobile web browsers (iOS Safari, Android Chrome)
4. **FR4:** The system shall automatically process uploaded photos by renaming with UUIDs, moving from staging (`raw_images/`) to display directory (`display_images/`), and triggering carousel updates
5. **FR5:** The system shall display uploaded photos on connected HDMI display in chronological carousel format (oldest first) with 7-second interval per photo
6. **FR6:** The carousel shall automatically detect new photos via hash comparison and dynamically update without requiring manual refresh or intervention
7. **FR7:** When no photos exist, the system shall display an instruction page with QR code for quick Wi-Fi/URL access and upload instructions
8. **FR8:** The system shall boot automatically on power connection and become fully operational within 3 minutes without manual intervention
9. **FR9:** The system shall store all uploaded photos persistently on local storage (500GB capacity target) with no external cloud dependency
10. **FR10:** The system shall provide a manual photo extraction mechanism (script or documented process) allowing venue staff to package all event photos for client delivery post-event
11. **FR11:** The upload interface shall provide immediate visual feedback confirming successful upload and estimated time to display appearance (10-15 second estimate)
12. **FR12:** The system shall handle photo orientation correctly, displaying images right-side-up regardless of device orientation during capture

## Non-Functional

1. **NFR1:** Photo processing pipeline shall achieve 95th percentile latency of ≤15 seconds from upload completion to carousel display appearance
2. **NFR2:** The system shall maintain 98% uptime during events (boot successfully and operate without critical failures in 98% of deployments)
3. **NFR3:** Wi-Fi network shall support 20 concurrent connections with <5% connection failure rate under normal venue conditions
4. **NFR4:** The upload interface shall be fully responsive and usable on smartphone screens (320px minimum width) across iOS and Android devices
5. **NFR5:** The carousel display shall support resolutions up to 4K (3840×2160) and gracefully scale photos to fit display dimensions
6. **NFR6:** System boot and initialization shall complete within 3 minutes from power-on to operational display state
7. **NFR7:** All data shall remain on local device with zero external network communication (offline-first architecture mandatory)
8. **NFR8:** Hardware platform shall be Raspberry Pi 4B (8GB RAM minimum) with 500GB storage, commercial-grade power supply, and ruggedized enclosure suitable for transport
9. **NFR9:** The system shall operate reliably in typical venue environments (temperature range 15-30°C, indoor use, standard AC power)
10. **NFR10:** Upload interface load time shall be <3 seconds on 3G/4G-equivalent local network connection
11. **NFR11:** The system shall implement automatic restart via systemd service management if core processes crash or hang
12. **NFR12:** Code and configuration shall be documented sufficiently for technical handoff, allowing third-party maintenance if required

---
