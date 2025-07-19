#!/bin/bash

# Create systemd service file
sudo tee /etc/systemd/system/dlmonitor.service << EOF
[Unit]
Description=DLMonitor Gunicorn Service
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/works/dlmonitor
Environment="PATH=/opt/miniconda3/envs/dlmonitor/bin/"
Environment="PYTHONPATH=/root/works/dlmonitor"
ExecStart=/opt/miniconda3/envs/dlmonitor/bin/gunicorn -w 8 --timeout 120 -b 0.0.0.0:8082 --access-logfile /var/log/dlmonitor-access.log --error-logfile /var/log/dlmonitor-error.log dlmonitor.webapp.app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create log directory if it doesn't exist
sudo mkdir -p /var/log
# Reload systemd daemon
sudo systemctl daemon-reload

# Stop service if running
sudo systemctl stop dlmonitor

# Enable and start service
sudo systemctl enable dlmonitor
sudo systemctl start dlmonitor

# Check status
sudo systemctl status dlmonitor