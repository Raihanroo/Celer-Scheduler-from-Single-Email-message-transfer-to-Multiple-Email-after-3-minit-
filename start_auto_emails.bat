@echo off
echo ========================================
echo Automatic Email Scheduler
echo ========================================
echo.
echo This will send scheduled emails automatically
echo Press Ctrl+C to stop
echo.
pause

python manage.py send_scheduled_emails --interval=60

pause
