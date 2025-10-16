#!/bin/bash
# Installation script for image-share systemd service
# Run with: sudo bash scripts/install-service.sh

set -e

echo "=== Image-Share Service Installation ==="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "ERROR: Please run as root (use sudo)"
    exit 1
fi

# Define paths
SERVICE_FILE="infrastructure/image-share.service"
SYSTEMD_PATH="/etc/systemd/system/image-share.service"
PROJECT_DIR="/home/pi/image-share"
SERVICE_USER="pi"

echo "Step 1: Copying service file to systemd directory..."
if [ ! -f "$SERVICE_FILE" ]; then
    echo "ERROR: Service file not found at $SERVICE_FILE"
    exit 1
fi

cp "$SERVICE_FILE" "$SYSTEMD_PATH"
chmod 644 "$SYSTEMD_PATH"
echo "✓ Service file installed at $SYSTEMD_PATH"

echo ""
echo "Step 2: Verifying service user exists..."
if ! id "$SERVICE_USER" &>/dev/null; then
    echo "ERROR: User '$SERVICE_USER' does not exist"
    exit 1
fi
echo "✓ User '$SERVICE_USER' exists"

echo ""
echo "Step 3: Setting project directory ownership..."
if [ -d "$PROJECT_DIR" ]; then
    chown -R "$SERVICE_USER:$SERVICE_USER" "$PROJECT_DIR"
    echo "✓ Ownership set to $SERVICE_USER:$SERVICE_USER"
else
    echo "WARNING: Project directory $PROJECT_DIR not found"
    echo "Make sure to deploy the project to $PROJECT_DIR before starting the service"
fi

echo ""
echo "Step 4: Verifying image directories..."
IMAGE_DIRS=(
    "/image-share-data/raw_images"
    "/image-share-data/display_images"
    "/image-share-data/failed_images"
)

for dir in "${IMAGE_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "Creating directory: $dir"
        mkdir -p "$dir"
    fi
    chown -R "$SERVICE_USER:$SERVICE_USER" "$dir"
    chmod -R 755 "$dir"
done
echo "✓ Image directories configured"

echo ""
echo "Step 5: Reloading systemd daemon..."
systemctl daemon-reload
echo "✓ Systemd daemon reloaded"

echo ""
echo "Step 6: Enabling service for boot startup..."
systemctl enable image-share.service
echo "✓ Service enabled"

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Next steps:"
echo "  1. Ensure .env file exists at: $PROJECT_DIR/apps/api/.env"
echo "  2. Start the service: sudo systemctl start image-share.service"
echo "  3. Check status: sudo systemctl status image-share.service"
echo "  4. View logs: sudo journalctl -u image-share.service -f"
echo ""
