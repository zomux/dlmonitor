#!/bin/bash

# Nginx management script for dlmonitor

case "$1" in
    start)
        echo "Starting nginx..."
        sudo systemctl start nginx
        ;;
    stop)
        echo "Stopping nginx..."
        sudo systemctl stop nginx
        ;;
    restart)
        echo "Restarting nginx..."
        sudo systemctl restart nginx
        ;;
    reload)
        echo "Reloading nginx configuration..."
        sudo systemctl reload nginx
        ;;
    status)
        echo "Checking nginx status..."
        sudo systemctl status nginx
        ;;
    test)
        echo "Testing nginx configuration..."
        sudo nginx -t
        ;;
    logs)
        echo "Showing nginx logs for dlmonitor..."
        echo "=== Access Logs ==="
        sudo tail -n 20 /var/log/nginx/dlmonitor.access.log
        echo ""
        echo "=== Error Logs ==="
        sudo tail -n 20 /var/log/nginx/dlmonitor.error.log
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|reload|status|test|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start nginx service"
        echo "  stop    - Stop nginx service"
        echo "  restart - Restart nginx service"
        echo "  reload  - Reload nginx configuration"
        echo "  status  - Show nginx service status"
        echo "  test    - Test nginx configuration"
        echo "  logs    - Show recent dlmonitor nginx logs"
        exit 1
        ;;
esac 