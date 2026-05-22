#!/bin/bash
# Initial ECS server setup — run ONCE on the server as root
set -e

echo "=== Installing system packages ==="
yum install -y python3 python3-devel python3-pip mysql-devel gcc nginx

echo "=== Creating app directory ==="
mkdir -p /opt/flask-app/logs

echo "=== Setting up Python virtualenv ==="
python3 -m venv /opt/flask-app/venv

echo "=== Installing systemd service ==="
cp "$(dirname "$0")/flask-app.service" /etc/systemd/system/flask-app.service
systemctl daemon-reload
systemctl enable flask-app

echo "=== Configuring firewall ==="
firewall-cmd --permanent --add-port=5000/tcp 2>/dev/null || true
firewall-cmd --reload 2>/dev/null || true

echo "=== Done ==="
echo "Place .env file at /opt/flask-app/.env before starting."
echo "Then: systemctl start flask-app"
