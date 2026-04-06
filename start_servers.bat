@echo off
echo ========================================
echo Django Email Scheduler - Quick Start
echo ========================================
echo.
echo এই script 3টি terminal window খুলবে:
echo 1. Django Server
echo 2. Celery Worker
echo 3. Celery Beat
echo.
pause

echo Starting Django Server...
start cmd /k "title Django Server && python manage.py runserver"

timeout /t 2 /nobreak >nul

echo Starting Celery Worker...
start cmd /k "title Celery Worker && celery -A core worker --loglevel=info --pool=solo"

timeout /t 2 /nobreak >nul

echo Starting Celery Beat...
start cmd /k "title Celery Beat && celery -A core beat --loglevel=info"

echo.
echo ========================================
echo সব server চালু হয়ে গেছে!
echo Browser এ যান: http://localhost:8000/
echo ========================================
