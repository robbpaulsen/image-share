# Image-Share Deployment Guide

This guide covers deploying and managing the Image-Share system on Raspberry Pi devices for production use at events.

## Table of Contents
- [Initial Deployment](#initial-deployment)
- [Service Management](#service-management)
- [Monitoring and Logs](#monitoring-and-logs)
- [Testing the Installation](#testing-the-installation)
- [Troubleshooting](#troubleshooting)

---

## Initial Deployment

### Prerequisites
- Raspberry Pi 4B with Raspberry Pi OS Lite (64-bit)
- Network connectivity for initial setup
- sudo/root access

### Step 1: Clone the Repository

```bash
git clone <repository-url> /home/pi/image-share
cd /home/pi/image-share
```

### Step 2: Create Virtual Environment and Install Dependencies

```bash
# Create virtual environment
uv venv

# Install dependencies
uv pip install -r apps/api/requirements.txt
```

### Step 3: Configure Environment Variables

Create the environment file at `/home/pi/image-share/apps/api/.env`:

```bash
LOG_LEVEL="INFO"
PHOTO_DIR_DISPLAY="/image-share-data/display_images"
PHOTO_DIR_RAW="/image-share-data/raw_images"
PHOTO_DIR_FAILED="/image-share-data/failed_images"
```

**IMPORTANT**: Never commit the `.env` file to version control.

### Step 4: Create Image Directories

```bash
sudo mkdir -p /image-share-data/raw_images
sudo mkdir -p /image-share-data/display_images
sudo mkdir -p /image-share-data/failed_images
sudo chown -R pi:pi /image-share-data
sudo chmod -R 755 /image-share-data
```

### Step 5: Install and Enable the Systemd Service

```bash
cd /home/pi/image-share
sudo bash scripts/install-service.sh
```

This script will:
- Copy the service file to `/etc/systemd/system/image-share.service`
- Set proper permissions on project files
- Enable the service for automatic startup on boot
- Configure image directories

### Step 6: Start the Service

```bash
sudo systemctl start image-share.service
```

**Note**: The service has a 3-minute startup delay to allow network initialization. Wait approximately 3.5 minutes before checking if the service is operational.

### Step 7: Verify Installation

```bash
# Check service status
sudo systemctl status image-share.service

# Run health check
bash scripts/health-check.sh
```

---

## Service Management

### Starting the Service

```bash
sudo systemctl start image-share.service
```

**Note**: After starting, wait 3 minutes for the startup delay before the service becomes operational.

### Stopping the Service

```bash
sudo systemctl stop image-share.service
```

### Restarting the Service

```bash
sudo systemctl restart image-share.service
```

**Note**: Restart also includes the 3-minute startup delay.

### Checking Service Status

```bash
sudo systemctl status image-share.service
```

Or use the convenience script:

```bash
bash scripts/service-status.sh
```

This shows:
- Service status (running/stopped/failed)
- Recent log entries
- Quick health check result

### Enabling/Disabling Auto-Start on Boot

Enable (default after installation):
```bash
sudo systemctl enable image-share.service
```

Disable:
```bash
sudo systemctl disable image-share.service
```

Check if enabled:
```bash
systemctl is-enabled image-share.service
```

---

## Monitoring and Logs

### Viewing Real-Time Logs

```bash
sudo journalctl -u image-share.service -f
```

Press `Ctrl+C` to stop following.

### Viewing Recent Logs

Last 100 lines:
```bash
sudo journalctl -u image-share.service -n 100
```

Last 20 lines (no pager):
```bash
sudo journalctl -u image-share.service -n 20 --no-pager
```

### Viewing Logs by Time

Since a specific time:
```bash
sudo journalctl -u image-share.service --since "2025-10-14 14:00:00"
```

Last 10 minutes:
```bash
sudo journalctl -u image-share.service --since "10 minutes ago"
```

Today's logs:
```bash
sudo journalctl -u image-share.service --since today
```

### Viewing Logs by Priority

Errors only:
```bash
sudo journalctl -u image-share.service -p err
```

Warnings and above:
```bash
sudo journalctl -u image-share.service -p warning
```

### Health Check

Manual health check:
```bash
bash scripts/health-check.sh
```

Expected output when healthy:
```
Checking service health at: http://localhost:8000/health
✓ Health check passed: Service is operational
  Response: {"status":"ok"}
```

---

## Testing the Installation

### Cold Boot Test

This verifies the system starts automatically after a complete power cycle:

1. Power off the Raspberry Pi:
   ```bash
   sudo shutdown -h now
   ```

2. Disconnect power and wait 10 seconds

3. Reconnect power and start timer

4. Wait 3.5 minutes for boot + network + service startup delay

5. Verify service is running:
   ```bash
   sudo systemctl status image-share.service
   bash scripts/health-check.sh
   ```

6. Test web interface accessibility:
   ```bash
   curl http://10.0.17.1:8000/health
   ```

**Expected Result**: Service operational within 3.5 minutes of power-on.

### Automatic Restart Test

This verifies the service automatically recovers from crashes:

1. Find the running process:
   ```bash
   sudo systemctl status image-share.service
   # Note the PID (Main PID: XXXX)
   ```

2. Kill the process forcefully:
   ```bash
   sudo kill -9 <PID>
   ```

3. Monitor service status:
   ```bash
   watch -n 1 'sudo systemctl status image-share.service'
   ```

4. Verify restart happens within 15 seconds (10s RestartSec + ~5s startup)

5. Confirm service is healthy again:
   ```bash
   bash scripts/health-check.sh
   ```

**Expected Result**: Service automatically restarts and becomes operational within 15 seconds.

---

## Troubleshooting

### Service Fails to Start

**Symptom**: `systemctl status` shows "failed" state

**Diagnosis**:
```bash
sudo journalctl -u image-share.service -n 50
```

**Common Causes**:

1. **Missing environment file**
   - Error: `EnvironmentFile=/home/pi/image-share/apps/api/.env not found`
   - Fix: Create the `.env` file with required variables (see Initial Deployment)

2. **Virtual environment not found**
   - Error: `Failed to execute command: No such file or directory`
   - Fix: Ensure virtual environment exists at `/home/pi/image-share/.venv`
   ```bash
   cd /home/pi/image-share
   uv venv
   uv pip install -r apps/api/requirements.txt
   ```

3. **Missing dependencies**
   - Error: `ModuleNotFoundError: No module named 'fastapi'`
   - Fix: Install dependencies in virtual environment
   ```bash
   cd /home/pi/image-share
   uv pip install -r apps/api/requirements.txt
   ```

### Permission Errors

**Symptom**: Errors about file access or directory creation

**Diagnosis**:
```bash
ls -la /home/pi/image-share
ls -la /image-share-data
```

**Fix**:
```bash
# Fix project directory ownership
sudo chown -R pi:pi /home/pi/image-share

# Fix image directory ownership
sudo chown -R pi:pi /image-share-data
sudo chmod -R 755 /image-share-data
```

### Port Binding Issues

**Symptom**: Error about address already in use

**Diagnosis**:
```bash
sudo netstat -tulpn | grep :8000
```

**Common Causes**:

1. **Another process using port 8000**
   - Fix: Stop the conflicting process or change port in service file

2. **Service already running**
   - Fix: Stop existing instance
   ```bash
   sudo systemctl stop image-share.service
   sudo systemctl start image-share.service
   ```

### Network Not Ready at Startup

**Symptom**: Service starts but can't access network resources

**Diagnosis**:
```bash
sudo journalctl -u image-share.service | grep -i network
```

**Fix**: Increase startup delay in service file

Edit `/etc/systemd/system/image-share.service`:
```ini
ExecStartPre=/bin/sleep 240  # Increase from 180 to 240 seconds
```

Then reload and restart:
```bash
sudo systemctl daemon-reload
sudo systemctl restart image-share.service
```

### Service Crashes After Startup

**Symptom**: Service starts but stops shortly after

**Diagnosis**:
```bash
sudo journalctl -u image-share.service -n 100
```

**Common Causes**:

1. **Application error (uncaught exception)**
   - Check logs for Python traceback
   - Fix: Debug application code

2. **Missing image directories**
   - Error: Directory not found
   - Fix: Create directories (see Initial Deployment Step 4)

3. **Database/storage issues**
   - Error: Permission denied or disk full
   - Fix: Check disk space and permissions

### Health Check Fails

**Symptom**: `health-check.sh` returns error

**Diagnosis**:
```bash
# Test direct connection
curl -v http://localhost:8000/health

# Check service is actually running
sudo systemctl status image-share.service

# Check for firewall issues
sudo iptables -L -n
```

**Common Causes**:

1. **Service not started yet** (within 3-minute delay)
   - Fix: Wait for startup delay to complete

2. **Wrong port in health check**
   - Fix: Verify port in service file matches health check URL

3. **Firewall blocking connection**
   - Fix: Configure firewall to allow port 8000
   ```bash
   sudo ufw allow 8000/tcp
   ```

### Checking Service Configuration

View the active service configuration:
```bash
sudo systemctl cat image-share.service
```

Verify service file syntax:
```bash
sudo systemd-analyze verify /etc/systemd/system/image-share.service
```

---

## Port Configuration Notes

The service runs on **port 8000** by default. To make it accessible on port 80 (standard HTTP), use one of these options:

### Option 1: iptables Port Forwarding (Recommended)

```bash
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8000
```

Make persistent:
```bash
sudo apt-get install iptables-persistent
sudo netfilter-persistent save
```

### Option 2: Grant Capability to Bind Port 80

```bash
sudo setcap 'cap_net_bind_service=+ep' /home/pi/image-share/.venv/bin/python
```

Then update service file to use port 80:
```ini
ExecStart=/home/pi/image-share/.venv/bin/uvicorn apps.api.main:app --host 0.0.0.0 --port 80
```

**Note**: Option 1 is recommended for security (service runs unprivileged).

---

## Additional Resources

- **Service File**: `infrastructure/image-share.service`
- **Installation Script**: `scripts/install-service.sh`
- **Health Check Script**: `scripts/health-check.sh`
- **Status Check Script**: `scripts/service-status.sh`
- **Application Logs**: `sudo journalctl -u image-share.service -f`
- **systemd Documentation**: `man systemd.service`

For development setup and testing, see the main [README.md](../README.md).
