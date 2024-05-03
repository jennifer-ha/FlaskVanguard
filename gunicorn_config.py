from multiprocessing import cpu_count
import os

# Basic configuration
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")  # The socket to bind. A tuple of (HOST, PORT) for TCP connections.
workers = int(os.getenv('GUNICORN_WORKERS', 2 * cpu_count() + 1)) # The number of worker processes. This number should generally be in the 2-4 x $(NUM_CORES) range.
accesslog = os.getenv("GUNICORN_ACCESS_LOG", "-") # Log access to stdout. Useful for debugging and monitoring.
errorlog = os.getenv("GUNICORN_ERROR_LOG", "-") # Log errors to stdout. Keeps error logs accessible in a standardized way.
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info") # Set log level to info. Consider "debug" for development and "warning" for production.

# Recommended additions for production
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "sync")  # Default is synchronous. For I/O-bound apps, consider 'gevent' or 'eventlet' for async workers.
timeout = int(os.getenv("GUNICORN_TIMEOUT", "30"))  # Workers silent for more than this many seconds are killed and restarted. Adjust as necessary.
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", "2")) # The number of seconds to wait for requests on a Keep-Alive connection. A higher value may be beneficial for keeping connections open longer for reuse.
preload_app = os.getenv("GUNICORN_PRELOAD_APP", "False") == "True" # Preload app code before worker fork. Set to True can save some RAM and improve startup time. Caution in development mode due to potential code reloading issues.

# Security settings for production
#secure_scheme_headers = {'X-FORWARDED-PROTO': 'https'}  # Comment in if behind a reverse proxy using HTTPS.
#forwarded_allow_ips = '*'  # Define a list of trusted proxies. '*' allows all. Be more restrictive in production.





