# Requirements & Dependencies

## System Requirements

### Development Environment
```
Operating System: Windows 10/11, macOS 10.15+, Ubuntu 20.04+
Python: 3.9+ (Recommended: 3.11)
Node.js: 16+ (for frontend tooling, optional)
Database: PostgreSQL 13+ (Production), SQLite 3.35+ (Development)
Memory: Minimum 4GB RAM, Recommended 8GB+
Storage: Minimum 2GB free space
```

### Production Environment
```
CPU: 2+ cores, 2.4GHz+
Memory: 8GB+ RAM
Storage: 50GB+ SSD
Database: PostgreSQL 13+ with 2GB+ allocated
Web Server: Nginx 1.18+ or Apache 2.4+
Python: 3.11+ with virtual environment
SSL Certificate: Required for production deployment
```

## Core Dependencies

### Base Requirements (requirements/base.txt)
```txt
# Django Framework
Django>=4.2.0,<5.0
djangorestframework>=3.14.0
django-cors-headers>=4.0.0
django-filter>=23.0.0
django-environ>=0.10.0

# Database
psycopg2-binary>=2.9.0
django-extensions>=3.2.0

# API Documentation
drf-spectacular>=0.26.0
drf-spectacular-sidecar>=2023.5.1

# Authentication & Security
djangorestframework-simplejwt>=5.2.0
django-allauth>=0.54.0
django-guardian>=2.4.0

# PDF Generation
weasyprint>=59.0
html5lib>=1.1
cairocffi>=1.4.0
cffi>=1.15.0

# File Handling
Pillow>=9.5.0
django-storages>=1.13.0

# Utilities
python-decouple>=3.8
pytz>=2023.3
python-dateutil>=2.8.0
```

### Development Requirements (requirements/development.txt)
```txt
-r base.txt

# Development Tools
django-debug-toolbar>=4.1.0
django-extensions>=3.2.0
ipython>=8.12.0
ipdb>=0.13.0

# Testing
pytest>=7.3.0
pytest-django>=4.5.0
pytest-cov>=4.1.0
factory-boy>=3.2.0
faker>=18.9.0

# Code Quality
black>=23.3.0
isort>=5.12.0
flake8>=6.0.0
mypy>=1.3.0
pre-commit>=3.3.0

# Performance
django-silk>=5.0.0
memory-profiler>=0.60.0

# Documentation
mkdocs>=1.4.0
mkdocs-material>=9.1.0
```

### Production Requirements (requirements/production.txt)
```txt
-r base.txt

# Production Web Server
gunicorn>=20.1.0
whitenoise>=6.4.0

# Monitoring & Logging
sentry-sdk>=1.25.0
django-health-check>=3.17.0

# Caching
redis>=4.5.0
django-redis>=5.2.0

# Performance
django-cachalot>=2.5.0
django-compressor>=4.3.1

# Background Tasks
celery>=5.2.0
django-celery-beat>=2.5.0
django-celery-results>=2.5.0

# Security
django-security>=0.18.0
django-csp>=3.7
```

### Testing Requirements (requirements/testing.txt)
```txt
-r base.txt

# Testing Framework
pytest>=7.3.0
pytest-django>=4.5.0
pytest-cov>=4.1.0
pytest-mock>=3.10.0
pytest-xdist>=3.3.0

# Test Data
factory-boy>=3.2.0
faker>=18.9.0

# API Testing
requests>=2.31.0
responses>=0.23.0

# Browser Testing (Optional)
selenium>=4.9.0
django-selenium>=0.9.8
```

## Frontend Dependencies

### CSS Framework (CDN)
```html
<!-- Bootstrap 5.3 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Icons -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
```

### JavaScript Libraries (CDN)
```html
<!-- Core Libraries -->
<script src="https://cdn.jsdelivr.net/npm/htmx.org@1.9.2/dist/htmx.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/alpinejs@3.12.0/dist/cdn.min.js" defer></script>

<!-- Charts -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.3.0/dist/chart.min.js"></script>

<!-- Utilities -->
<script src="https://cdn.jsdelivr.net/npm/moment@2.29.4/moment.min.js"></script>
```

### Optional Node.js Dependencies (package.json)
```json
{
  "name": "gadhawa-report-frontend",
  "version": "1.0.0",
  "description": "Frontend assets for gadhawa Report System",
  "scripts": {
    "build": "webpack --mode=production",
    "dev": "webpack --mode=development --watch",
    "sass": "sass --watch static/scss:static/css"
  },
  "devDependencies": {
    "sass": "^1.62.0",
    "webpack": "^5.85.0",
    "webpack-cli": "^5.1.0",
    "css-loader": "^6.8.0",
    "mini-css-extract-plugin": "^2.7.0"
  }
}
```

## Font Dependencies

### Nepali Fonts
```
Required Fonts for Nepali Language Support:
- Mukti (Primary Devanagari font)
- Kalimati (Alternative Devanagari font)
- Devanagari (System fallback)

Download Sources:
- Mukti: https://fonts.google.com/specimen/Mukti
- Kalimati: http://www.fonts2u.com/kalimati.font

Installation:
1. Download font files (.ttf, .woff, .woff2)
2. Place in static/fonts/ directory
3. Include in CSS @font-face declarations
```

### English Fonts
```
Primary: Inter (Variable font)
Source: https://fonts.google.com/specimen/Inter

Fallbacks:
- Segoe UI (Windows)
- SF Pro (macOS)
- Roboto (Android/Web)
- Sans-serif (System)
```

## Database Setup

### PostgreSQL Configuration
```sql
-- Create database
CREATE DATABASE gadhawa_report;
CREATE USER gadhawa_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE gadhawa_report TO gadhawa_user;

-- Extensions
\c gadhawa_report
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search
```

### Django Database Settings
```python
# settings/base.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='gadhawa_report'),
        'USER': env('DB_USER', default='gadhawa_user'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
        'OPTIONS': {
            'charset': 'utf8',
        },
    }
}
```

## Environment Variables

### .env Template
```bash
# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=gadhawa_report
DB_USER=gadhawa_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Redis (for caching and Celery)
REDIS_URL=redis://localhost:6379/0

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# File Storage
MEDIA_ROOT=media/
STATIC_ROOT=staticfiles/

# API Keys (if needed)
GOOGLE_MAPS_API_KEY=your-google-maps-key
WEATHER_API_KEY=your-weather-api-key

# Security (Production)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
X_FRAME_OPTIONS=DENY

# Sentry (Error Tracking)
SENTRY_DSN=your-sentry-dsn-here
```

## Installation Scripts

### setup.py (Project Setup)
```python
#!/usr/bin/env python3
"""
gadhawa Report System Setup Script
"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(command, check=True):
    """Run shell command with error handling"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=check,
            capture_output=True,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def setup_virtual_environment():
    """Create and activate virtual environment"""
    print("Setting up virtual environment...")
    
    if not Path("venv").exists():
        run_command("python -m venv venv")
    
    # Activation command varies by OS
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
    else:  # Unix/Linux/macOS
        activate_cmd = "source venv/bin/activate"
    
    print(f"Virtual environment created. Activate with: {activate_cmd}")

def install_dependencies():
    """Install Python dependencies"""
    print("Installing dependencies...")
    
    # Install base requirements
    run_command("pip install --upgrade pip")
    run_command("pip install -r requirements/development.txt")

def setup_database():
    """Setup database and run migrations"""
    print("Setting up database...")
    
    # Check if .env exists
    if not Path(".env").exists():
        print("Creating .env file from template...")
        run_command("cp .env.example .env")
        print("Please edit .env file with your configuration before proceeding.")
        return
    
    # Run migrations
    run_command("python manage.py migrate")
    
    # Create superuser (optional)
    response = input("Create superuser account? (y/n): ")
    if response.lower() == 'y':
        run_command("python manage.py createsuperuser", check=False)

def collect_static():
    """Collect static files"""
    print("Collecting static files...")
    run_command("python manage.py collectstatic --noinput")

def load_sample_data():
    """Load sample data for development"""
    response = input("Load sample data for development? (y/n): ")
    if response.lower() == 'y':
        print("Loading sample data...")
        run_command("python manage.py loaddata fixtures/sample_data.json")

def main():
    """Main setup function"""
    print("gadhawa Report System Setup")
    print("=" * 30)
    
    setup_virtual_environment()
    install_dependencies()
    setup_database()
    collect_static()
    load_sample_data()
    
    print("\nSetup completed successfully!")
    print("Start the development server with: python manage.py runserver")

if __name__ == "__main__":
    main()
```

### requirements-install.ps1 (Windows PowerShell)
```powershell
# Windows Installation Script
Write-Host "gadhawa Report System - Windows Setup" -ForegroundColor Green

# Check Python version
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Python is not installed or not in PATH"
    exit 1
}

Write-Host "Found Python: $pythonVersion" -ForegroundColor Blue

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements/development.txt

# Copy environment file
if (!(Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "Please edit .env file with your configuration" -ForegroundColor Red
}

Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your configuration" -ForegroundColor White
Write-Host "2. Run: python manage.py migrate" -ForegroundColor White
Write-Host "3. Run: python manage.py runserver" -ForegroundColor White
```

### install.sh (Linux/macOS Bash)
```bash
#!/bin/bash
# Linux/macOS Installation Script

echo "gadhawa Report System - Linux/macOS Setup"
echo "=========================================="

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Found Python: $PYTHON_VERSION"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements/development.txt

# Copy environment file
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit .env file with your configuration"
fi

echo "Setup completed successfully!"
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python manage.py migrate"
echo "4. Run: python manage.py runserver"
```

## Docker Configuration (Optional)

### Dockerfile
```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        libcairo2-dev \
        libpango1.0-dev \
        libgdk-pixbuf2.0-dev \
        libffi-dev \
        shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements/ ./requirements/
RUN pip install --no-cache-dir -r requirements/production.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "gadhawa_report.wsgi:application"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: gadhawa_report
      POSTGRES_USER: gadhawa_user
      POSTGRES_PASSWORD: your_secure_password

  redis:
    image: redis:7-alpine

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/0

volumes:
  postgres_data:
```

This comprehensive requirements specification provides everything needed to set up and run the gadhawa Digital Profile Report system across different environments and platforms.
