# Brainstorming Session Results

## Session Setup

*   **Topic:** Application workflow, listing first and next steps.
*   **Constraints:** Hardware is a Raspberry Pi 4B (8GB RAM, 500GB storage).
*   **Goal:** Focused ideation on implementing each stage of the workflow described in README.md.
*   **Output:** Yes, a structured document.

## Approach

*   **Selected Approach:** 2. Analyst recommends techniques based on context.
*   **Recommended Technique:** 4. First Principles Thinking

---

# Technique: First Principles Thinking

## Backend Workflow

### Step 1: Manual Server Initiation

*   **User Input:** The Raspberry Pi has no battery, so it must be plugged in at the event. The application should start automatically after boot.
*   **First Principles Identified:**
    1.  **Physical Power:** The device must be physically connected to a power source at the event location.
    2.  **OS Boot:** The Raspberry Pi's operating system must boot successfully after receiving power.
    3.  **Application Auto-run:** A mechanism (e.g., systemd service, startup script) must be configured to automatically launch the server application after the OS is fully booted.

### Step 2: The server starts an access point

*   **User Input:** The device is already pre-configured to act as an offline router.
*   **First Principles Identified:**
    1.  **Physical Connectivity:** The Wi-Fi antenna must be physically connected and functional.
    2.  **Master Network Configuration:** The OS is configured to start in Access Point mode on the `wlan0` interface.
    3.  **Essential Network Services:** The following services and configurations must be correctly established and loaded to operate as a standalone router:
        *   **Server IP Assignment:** `dhcpcd.conf` for managing the static IP of the device itself.
        *   **Access Point Software:** `hostapd.conf` to manage the creation of the Wi-Fi network (SSID, password, etc.).
        *   **DHCP Server:** `dnsmasq.conf` to assign IP addresses to connecting clients.
        *   **DNS Server:** `dnsmasq.conf` also handles DNS requests for the local network.
        *   **Firewall & Routing Rules:** `iptables` and `sysctl.conf` to manage network traffic and packet forwarding.

### Step 3: The main application starts automatically after 3 minutes

*   **User Input:** The application must be started with a timer after boot, and the dependencies must be ready. The best timing mechanism is unknown.
*   **First Principles Identified:**
    1.  **Application Integrity:** All dependencies, libraries, and components of the application (frontend and backend) must be pre-installed and correctly configured on the device.
    2.  **Timed Start-up Mechanism:** A system-level service must be configured to invoke the application's launch.
        *   **Trigger:** The service is activated upon system boot completion.
        *   **Delay:** The service must wait for a defined period (3 minutes) before executing the start command.
        *   **Execution:** The service runs the command or script that launches the main application's web server. (A `systemd` timer is an ideal solution for this logic).

### Step 4 (Revised): The application operates in a static and known network environment

*   **User Input:** The application's functionality to manage the access point was removed. The device now permanently functions as a router with a fixed network configuration.
*   **First Principles Identified:**
    1.  **Persistent Network State:** The device always boots and operates in router/access point mode. There is no "no network" state.
    2.  **Static IP Address:** The application can safely assume that its gateway IP address (the server's own address) is always `10.0.17.1`. No dynamic query is required.
    3.  **Fixed Subnet Configuration:** The network operates on the `10.0.17.1/24` subnet, with a DHCP range limited to 20 clients via `dnsmasq`.
    4.  **Implication:** The application logic is simplified, as the server address and network state values are constants that can be hardcoded or read from a configuration file, eliminating the need for runtime probes.

---

## Backend Subprocesses

### Subprocess 1: Monitoring and Processing New Images

*   **User Input:** The system must detect and process new uploaded images. The approach is based on moving files between directories that represent their state.
*   **First Principles Identified:**
    1.  **Defined Directory Structure:** A folder structure is established to manage the state of the images:
        *   `raw_images/`: A "staging" directory where all user-uploaded images are initially saved.
        *   `display_images/`: A "processed" directory containing images that have been renamed and are ready to be displayed.
    2.  **State-Based Definition of "Newness":** An image is considered "new" and requires processing if, and only if, it exists in the `raw_images/` directory.
    3.  **Periodic Processing Loop:** A timing mechanism (e.g., a `setInterval` loop or a `ScheduledExecutorService`) runs every 10 seconds to initiate the verification process.
    4.  **Fundamental Processing Logic:** The core of the process relies on file system operations, accessible through standard programming language libraries:
        *   **Detection:** The service lists the contents of the `raw_images/` directory.
        *   **Processing:** If files are found, for each file:
            *   A Universally Unique Identifier (UUID) is generated.
            *   The rename/move function (`rename`/`move`) transfers the file from `raw_images/` to `display_images/`, applying the new name `[UUID].[extension]`.
    5.  **Hand-off of Responsibility:** Once a file reaches `display_images/`, it is considered processed by this subprocess, and the responsibility for displaying it passes to another subprocess (the `display_reel`).

### Subprocess 2: Image Display Carousel

*   **User Input:** The system must display an image carousel if images exist, or an upload page if not. The order should reflect when images were uploaded, and the carousel should update if new photos are added.
*   **First Principles Identified:**
    1.  **View Bifurcation Logic (Backend):** An API endpoint (e.g., `/api/v1/reel-state`) is needed to encapsulate the state logic.
        *   **Action:** This endpoint checks the number of files in the `display_images/` directory.
        *   **Response:**
            *   If the count is `0`, it returns a state instructing the frontend to show the `[carga_tu_imagen]` page.
            *   If the count is `> 0`, it returns a state to show the carousel, along with the sorted list of image files and the list's hash.
    2.  **Relevance Sorting (Backend):** To ensure a fair order, files in `display_images/` are not sorted alphabetically (which would be random with UUIDs), but by their **modification or creation timestamp**. This ensures older images are shown first.
    3.  **Efficient Update Mechanism (Backend/Frontend):**
        *   **Backend:** The `/api/v1/reel-state` endpoint calculates a **MD5 hash** of the sorted list of filenames. This hash uniquely and quickly represents the current state of the carousel.
        *   **Frontend:** The frontend stores the last received hash. Periodically (e.g., every 15-30 seconds), it calls the endpoint again. If the new hash is different from what it has, it requests the new image list and integrates it into the carousel. If the hash is the same, it does nothing.
    4.  **Display Logic (Frontend):**
        *   **Carousel Loop:** A JavaScript function on the client manages the carousel. It keeps an index of the current image in the list.
        *   **Timer:** `setInterval` or `setTimeout` is used to change the visible image every 7 seconds, updating the `src` of an `<img>` element.
        *   **Loop Reset:** When the carousel reaches the end of the list, it simply returns to index `0` to start over.

### Subprocess 3: Post-Event Data Extraction

*   **User Input:** A method is needed to archive all event images for the host. The process must be safe and manual to prevent data loss.
*   **First Principles Identified:**
    1.  **Manual and External Execution:** The process is encapsulated in a **separate script**, not part of the main event application. It is run manually in a controlled environment ("at base") after the event.
    2.  **Redundancy Principle (Backup):** The script's first action is to create a full backup of the `display_images/` directory. This ensures no risk of data loss during the compression process.
    3.  **Compression and Packaging:**
        *   **Action:** The script uses a system utility (like `zip`) to create a single compressed file.
        *   **Contents:** The `.zip` file contains both the original `display_images/` directory and its backup.
        *   **Format:** The `.zip` format is chosen for its universal compatibility with end-user operating systems (Windows, macOS).
    4.  **Organized Output Location:** The resulting `.zip` file is saved to a dedicated directory, `zipped_images/`, to keep the project organized.
    5.  **Safe Manual Transfer:** The final transfer of the `.zip` file from the `zipped_images/` directory to a USB storage drive is done **manually**. This deliberate choice avoids running automated destructive commands (like `dd` or `rm`) on the wrong storage devices.