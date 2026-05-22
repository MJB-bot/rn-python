#!/bin/bash
# Deploy script — runs on ECS server from GitHub Actions SSH
set -e

APP_DIR="/opt/flask-app"

echo "=== Activating virtualenv ==="
source $APP_DIR/venv/bin/activate

echo "=== Installing dependencies ==="
pip install -r $APP_DIR/requirements.txt

echo "=== Restarting Flask ==="
systemctl restart flask-app

echo "=== Checking status ==="
sleep 2
systemctl status flask-app --no-pager

echo "=== Health check ==="
curl -s http://localhost:5000/api/health || echo "Health check failed, check logs"

echo "=== Deploy complete ==="
