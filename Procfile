web: gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A core worker --loglevel=info
beat: python manage.py migrate && celery -A core beat --loglevel=info
