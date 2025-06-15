#!/bin/bash
# Development server startup script for lungri Report System

echo "Starting lungri Digital Profile Report System..."
echo

# Activate virtual environment
source venv/bin/activate

# Run migrations (in case there are new ones)
echo "Checking for new migrations..."
python manage.py migrate

echo
echo "Starting development server..."
echo "Access the system at: http://127.0.0.1:8000"
echo "API Documentation at: http://127.0.0.1:8000/api/docs/"
echo "Admin Interface at: http://127.0.0.1:8000/admin/"
echo

python manage.py runserver
