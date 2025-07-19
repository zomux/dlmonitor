#!/bin/bash

# Fix permissions script for dlmonitor static files
# This script ensures nginx (www-data) can access static files

echo "Fixing permissions for dlmonitor static files..."

# Fix directory permissions (755 = rwxr-xr-x)
# This allows nginx to traverse directories
echo "Setting directory permissions..."
sudo chmod 755 /root
sudo chmod 755 /root/works
sudo chmod -R 755 /root/works/dlmonitor

# Fix static file permissions (644 = rw-r--r--)
# This allows nginx to read static files
echo "Setting static file permissions..."
sudo chmod -R 644 /root/works/dlmonitor/dlmonitor/webapp/static/*

# Ensure static directories are executable (755 = rwxr-xr-x)
# This allows nginx to access directories
echo "Setting static directory permissions..."
sudo chmod 755 /root/works/dlmonitor/dlmonitor/webapp/static/
if [[ -d "/root/works/dlmonitor/dlmonitor/webapp/static/fonts" ]]; then
    sudo chmod 755 /root/works/dlmonitor/dlmonitor/webapp/static/fonts/
fi

# Reload nginx to ensure changes take effect
echo "Reloading nginx..."
sudo systemctl reload nginx

# Test static file access
echo "Testing static file access..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost/static/default.css | grep -q "200"; then
    echo "✓ Static files are accessible"
    echo "✓ Permissions fixed successfully"
else
    echo "✗ Static files still not accessible"
    echo "Please check nginx error logs: sudo tail -f /var/log/nginx/dlmonitor.error.log"
    exit 1
fi

echo "Done! Static files should now be accessible via nginx." 