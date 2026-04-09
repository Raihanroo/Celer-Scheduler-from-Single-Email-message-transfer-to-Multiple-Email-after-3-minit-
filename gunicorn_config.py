# Gunicorn configuration for Render free tier
import multiprocessing

# Bind to the port provided by Render
bind = "0.0.0.0:10000"

# Worker configuration - optimized for 512MB RAM
workers = 1  # Only 1 worker for free tier
worker_class = "sync"
worker_connections = 1000
timeout = 120  # Increased timeout
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "django_email_scheduler"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Memory management
max_requests = 1000  # Restart worker after 1000 requests
max_requests_jitter = 50
