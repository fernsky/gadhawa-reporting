#!/bin/bash
# Activation script for Lungri Report System
# This ensures the correct Django settings module is loaded

echo "🚀 Activating Lungri Report System environment..."

# Activate virtual environment
source .venv/bin/activate

# Set Django settings module
export DJANGO_SETTINGS_MODULE=lungri_report.settings.development

# Clear any cached Python files
echo "🧹 Clearing Python cache..."
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

echo "✅ Environment activated!"
echo "💡 Django settings: $DJANGO_SETTINGS_MODULE"
echo ""
echo "You can now run Django commands like:"
echo "  python manage.py runserver"
echo "  python manage.py check"
echo "  python manage.py migrate"
echo ""
