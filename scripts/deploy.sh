#!/bin/bash

# Define variables
REMOTE_USER="root"
REMOTE_HOST="deeplearn2"
REMOTE_PATH="/root/works/dlmonitor"
LOCAL_PATH="."

# Ensure script is run from project root
if [[ ! -d "dlmonitor" ]]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Generate a random number between 100000 and 999999 save to configs/deployment.json
RANDOM_NUMBER=`jot -r 1 100000 999999`
echo "{\"random_number\": $RANDOM_NUMBER}" > configs/deployment.json

# Sync files to remote server
echo "Deploying to $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH..."
rsync -avz --exclude '.git' \
           --exclude '__pycache__' \
           --exclude '*.pyc' \
           --exclude 'venv' \
           --exclude '.env' \
           --exclude '.gitignore' \
           --exclude '.DS_Store' \
           --exclude 'cache' \
           $LOCAL_PATH $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH

# Check if rsync was successful
if [ $? -eq 0 ]; then
    echo "Deployment successful!"
else
    echo "Error: Deployment failed"
    exit 1
fi

# SSH into remote server, fix permissions, and restart service
echo "Fixing permissions and restarting service on remote server..."
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && bash scripts/fix_permissions.sh && bash scripts/launch_server.sh"

# Check if SSH command was successful
if [ $? -eq 0 ]; then
    echo "Service restart successful!"
else
    echo "Error: Service restart failed"
    exit 1
fi

# Git push
git push