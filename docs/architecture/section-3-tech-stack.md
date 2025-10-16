# Section 3: Tech Stack

### **Technology Stack Table**

| Category | Technology | Version | Purpose | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend Language** | JavaScript | ES2021+ | Core UI Logic | Universal browser compatibility, lightweight, and avoids complex build steps. |
| **Frontend Framework**| Vanilla JS | N/A | UI Application | Ensures the absolute minimum bundle size and fastest possible load time, which is critical for the mobile upload interface. |
| **UI Component Library**| None | N/A | UI Components | Custom, minimal CSS will be used. Avoids overhead of a library for a very simple UI. |
| **State Management** | Local Component State | N/A | Manage UI State | The application's state is simple enough that a dedicated library like Redux or Zustand is unnecessary overhead. |
| **Backend Language** | Python | 3.10+ | Server-side Logic | Mature, excellent for file system operations and system scripting, with a strong ecosystem for image processing. |
| **Backend Framework** | FastAPI | Latest | API & Web Server | Provides high performance for concurrent uploads (async) and automatic API documentation, as suggested in the PRD. |
| **API Style** | REST | OpenAPI 3.0 | Client-Server Communication | Simple, widely understood standard. FastAPI generates the OpenAPI specification automatically, aiding development. |
| **Database** | Filesystem | N/A | Data Persistence | A core architectural decision to reduce dependencies and complexity, sufficient for the project's scale. |
| **File Storage** | Local SSD | 500GB+ | Photo Storage | Provides fast and reliable storage for images, as required by the PRD. |
| **Authentication** | None | N/A | User Access Control | Core requirement for a zero-friction guest experience on an isolated, trusted network. |
| **Backend Testing** | pytest | Latest | Unit & Integration Tests | The standard, powerful testing framework for the Python ecosystem. |
| **E2E Testing** | Manual & Scripted | N/A | System Validation | Full automated E2E is too complex for the MVP. Critical paths will be validated via scripts and manual testing. |
| **IaC Tool** | Ansible / Shell Script | Latest | Pi Provisioning | Enables automated, repeatable setup of the Raspberry Pi devices from a clean OS install. |
| **Process Manager** | systemd | OS-provided | Service Management | Robust, built-in OS tool for ensuring the backend process runs on boot and restarts on failure. |
| **Monitoring** | journalctl | OS-provided | Log Aggregation | The standard systemd interface for viewing service logs on the device. |
| **Logging** | Python Logging Module | 3.10+ | Application Logging | Flexible standard library for structured logging to the systemd journal or local files. |
| **CSS Framework** | Custom CSS | N/A | Styling | Guarantees the smallest possible CSS payload for the fastest mobile experience. |

---