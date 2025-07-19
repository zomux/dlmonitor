#!/bin/bash
#
# Run this find directly on server.
#
source .env

mkdir -p /etc/supervisor/conf.d/
mkdir -p /var/logs/gunicorn/

cp deployment/nginx.conf /etc/nginx/sites-enabled/nginx_dlmonitor.conf
cat deployment/supervisor.conf | sed -E "s/PASSWD/${SUPERVISORD_PASSWD}/g" > /etc/supervisor/conf.d/supervisord.conf
