# Scripts Directory

This directory contains operational scripts for deploying and managing the Image-Share system on Raspberry Pi.

## Available Scripts

### `install-service.sh`
**Purpose**: Automated installation script for the systemd service

**Usage**:
```bash
sudo bash scripts/install-service.sh
```

**What it does**:
- Copies service file to systemd directory
- Sets proper permissions on service file
- Configures project directory ownership
- Creates and configures image directories
- Reloads systemd daemon
- Enables service for boot startup

**Requirements**: Must be run as root (use sudo)

---

### `health-check.sh`
**Purpose**: Validates that the service is responding correctly

**Usage**:
```bash
bash scripts/health-check.sh
```

**What it does**:
- Performs HTTP GET to service health endpoint
- Validates JSON response structure
- Returns exit code 0 on success, 1 on failure

**Environment Variables**:
- `HEALTH_URL` - Override default health check URL (default: http://localhost:8000/health)

**Example**:
```bash
HEALTH_URL=http://10.0.17.1:8000/health bash scripts/health-check.sh
```

---

### `service-status.sh`
**Purpose**: Quick status overview of the service

**Usage**:
```bash
bash scripts/service-status.sh
```

**What it does**:
- Shows systemd service status
- Displays recent log entries (last 20 lines)
- Runs health check

**Output**: Combined view of service state, logs, and health status

---

## Script Permissions

All scripts should be executable. To set permissions:

```bash
chmod +x scripts/*.sh
```

## Related Documentation

For complete deployment instructions, see [docs/deployment.md](../docs/deployment.md)
