#!/bin/bash
# Health check script for image-share service
# Validates that the service is responding correctly
# Exit code: 0 = success, 1 = failure

# Configuration
HEALTH_URL="${HEALTH_URL:-http://localhost:8000/health}"
TIMEOUT=5

# Perform health check
echo "Checking service health at: $HEALTH_URL"
RESPONSE=$(curl -s -m "$TIMEOUT" "$HEALTH_URL" 2>&1)
CURL_EXIT=$?

# Check if curl succeeded
if [ $CURL_EXIT -ne 0 ]; then
    echo "✗ Health check failed: Unable to connect to service"
    echo "  Curl error code: $CURL_EXIT"
    echo "  Error: $RESPONSE"
    exit 1
fi

# Parse and validate JSON response
STATUS=$(echo "$RESPONSE" | grep -o '"status":"ok"' || echo "")

if [ -n "$STATUS" ]; then
    echo "✓ Health check passed: Service is operational"
    echo "  Response: $RESPONSE"
    exit 0
else
    echo "✗ Health check failed: Service not responding correctly"
    echo "  Response: $RESPONSE"
    exit 1
fi
