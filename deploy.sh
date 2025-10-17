#!/bin/bash

PROJECT_DIR="/home/ubuntu/todo_mvp" 
VENV_PATH="/home/ubuntu/venv/bin/python"

cd $PROJECT_DIR || exit

echo "Pulling latest code..."
git pull origin main
echo "Installing dependencies..."
$VENV_PATH -m pip install -r requirements.txt

echo "Running migrations..."
$VENV_PATH manage.py migrate --noinput

echo "Collecting static files..."
$VENV_PATH manage.py collectstatic --noinput

echo "Restarting Gunicorn..."
sudo systemctl restart gunicorn

echo "Reloading Nginx..."
sudo systemctl reload nginx

echo "Deployment complete!"