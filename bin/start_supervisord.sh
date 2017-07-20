#!/bin/bash
supervisord -c /etc/supervisor/conf.d/supervisord.conf
supervisorctl -c /etc/supervisor/conf.d/supervisord.conf restart dlmonitor
