#!/bin/bash

# Cron management script for dlmonitor fetch_new_sources

CRON_ENTRY='30 * * * * ({ PYTHONPATH="/root/works/dlmonitor" /opt/miniconda3/envs/dlmonitor/bin/python /root/works/dlmonitor/bin/fetch_new_sources.py all; } | tee /tmp/1cxcTJCSsvy8LIA3.stdout) 3>&1 1>&2 2>&3 | tee /tmp/1cxcTJCSsvy8LIA3.stderr'
CRON_COMMENT="# DLMonitor - Fetch new sources every 30 minutes"

# Function to check if cron job exists
check_cron() {
    if crontab -l 2>/dev/null | grep -F "fetch_new_sources.py" >/dev/null; then
        echo "✓ Cron job exists"
        echo "Current cron jobs related to dlmonitor:"
        crontab -l 2>/dev/null | grep -E "(fetch_new_sources|DLMonitor)"
        return 0
    else
        echo "✗ Cron job not found"
        return 1
    fi
}

# Function to add cron job
add_cron() {
    echo "Adding cron job for dlmonitor fetch_new_sources..."
    
    # Check if it already exists
    if check_cron >/dev/null 2>&1; then
        echo "Warning: Cron job already exists. Use 'remove' first if you want to replace it."
        return 1
    fi
    
    # Create a temporary file with current crontab + new entry
    TEMP_CRON=$(mktemp)
    
    # Get existing crontab (ignore errors if no crontab exists)
    crontab -l 2>/dev/null > "$TEMP_CRON" || true
    
    # Add comment and cron entry
    echo "" >> "$TEMP_CRON"
    echo "$CRON_COMMENT" >> "$TEMP_CRON"
    echo "$CRON_ENTRY" >> "$TEMP_CRON"
    
    # Install the new crontab
    if crontab "$TEMP_CRON"; then
        echo "✓ Cron job added successfully"
        echo "The script will run every 30 minutes to fetch new sources"
    else
        echo "✗ Failed to add cron job"
        rm -f "$TEMP_CRON"
        return 1
    fi
    
    # Clean up
    rm -f "$TEMP_CRON"
}

# Function to remove cron job
remove_cron() {
    echo "Removing cron job for dlmonitor fetch_new_sources..."
    
    # Check if it exists
    if ! check_cron >/dev/null 2>&1; then
        echo "No cron job found to remove"
        return 1
    fi
    
    # Create a temporary file with current crontab minus the dlmonitor entries
    TEMP_CRON=$(mktemp)
    
    # Get existing crontab and filter out dlmonitor entries
    crontab -l 2>/dev/null | grep -v -E "(fetch_new_sources|DLMonitor)" > "$TEMP_CRON"
    
    # Install the modified crontab
    if crontab "$TEMP_CRON"; then
        echo "✓ Cron job removed successfully"
    else
        echo "✗ Failed to remove cron job"
        rm -f "$TEMP_CRON"
        return 1
    fi
    
    # Clean up
    rm -f "$TEMP_CRON"
}

# Function to test the fetch script
test_fetch() {
    echo "Testing the fetch_new_sources.py script..."
    echo "Running: PYTHONPATH=\"/root/works/dlmonitor\" /opt/miniconda3/envs/dlmonitor/bin/python /root/works/dlmonitor/bin/fetch_new_sources.py all"
    
    cd /root/works/dlmonitor
    PYTHONPATH="/root/works/dlmonitor" /opt/miniconda3/envs/dlmonitor/bin/python /root/works/dlmonitor/bin/fetch_new_sources.py all
    
    echo "Test completed with exit code: $?"
}

# Function to show logs
show_logs() {
    echo "Recent stdout logs:"
    if [[ -f /tmp/1cxcTJCSsvy8LIA3.stdout ]]; then
        echo "=== Last 20 lines of stdout ==="
        tail -n 20 /tmp/1cxcTJCSsvy8LIA3.stdout
    else
        echo "No stdout log file found"
    fi
    
    echo ""
    echo "Recent stderr logs:"
    if [[ -f /tmp/1cxcTJCSsvy8LIA3.stderr ]]; then
        echo "=== Last 20 lines of stderr ==="
        tail -n 20 /tmp/1cxcTJCSsvy8LIA3.stderr
    else
        echo "No stderr log file found"
    fi
}

# Function to show all cron jobs
show_all_cron() {
    echo "All current cron jobs:"
    crontab -l 2>/dev/null || echo "No cron jobs found"
}

# Main script logic
case "$1" in
    add)
        add_cron
        ;;
    remove)
        remove_cron
        ;;
    check)
        check_cron
        ;;
    test)
        test_fetch
        ;;
    logs)
        show_logs
        ;;
    list)
        show_all_cron
        ;;
    *)
        echo "Usage: $0 {add|remove|check|test|logs|list}"
        echo ""
        echo "Commands:"
        echo "  add     - Add the cron job for fetch_new_sources"
        echo "  remove  - Remove the cron job"
        echo "  check   - Check if the cron job exists"
        echo "  test    - Test run the fetch_new_sources script"
        echo "  logs    - Show recent execution logs"
        echo "  list    - Show all current cron jobs"
        echo ""
        echo "The cron job will run every 30 minutes and execute:"
        echo "  /opt/miniconda3/envs/dlmonitor/bin/python /root/works/dlmonitor/bin/fetch_new_sources.py all"
        exit 1
        ;;
esac 