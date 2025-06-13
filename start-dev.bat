@echo off
REM Development server startup script for Gadhawa Report System

echo Starting Gadhawa Digital Profile Report System...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run migrations (in case there are new ones)
echo Checking for new migrations...
python manage.py migrate

echo.
echo Starting development server...
echo Access the system at: http://127.0.0.1:8000
echo API Documentation at: http://127.0.0.1:8000/api/docs/
echo Admin Interface at: http://127.0.0.1:8000/admin/
echo.

python manage.py runserver
