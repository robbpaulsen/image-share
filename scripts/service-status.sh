#!/bin/bash
# Quick service status check script
# Shows service status and recent logs

echo "=== Image-Share Service Status ==="
echo ""

# Check service status
systemctl status image-share.service --no-pager

echo ""
echo "=== Recent Logs (last 20 lines) ==="
journalctl -u image-share.service -n 20 --no-pager

echo ""
echo "=== Quick Health Check ==="
bash "$(dirname "$0")/health-check.sh" || true
