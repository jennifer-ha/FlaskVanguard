# extensions.py
from flask_limiter import Limiter
from app.utils import limit_key, should_compress  
import redis
from flask_compress import Compress
from flask_cors import CORS
import logging
from flask_talisman import Talisman

# Initialize the Compress extension
compress = Compress()

class RateLimiter:
    """
    A class used to represent a rate limiter for a Flask application.

    This class wraps the Flask-Limiter extension and provides a way to initialize it with a custom key function and storage URI.

    Attributes:
        _limiter (flask_limiter.Limiter): The underlying Flask-Limiter instance.

    Methods:
        __init__(app: Flask, storage_uri: str = None): Initializes the rate limiter.
    """
    from redis.exceptions import RedisError
from flask_limiter.util import ConfigurationError

def __init__(self, app, storage_uri=None):
    """
    Initialize the rate limiter for the given Flask application.

    This function initializes a Flask-Limiter instance with a custom key function and storage URI. 
    The storage URI is retrieved from the application's configuration using the 'STORAGE_URL' key. 
    If the storage URI starts with "redis://", it attempts to connect to Redis and logs a message if successful.

    Args:
        app (Flask): The Flask application instance.
        storage_uri (str, optional): The storage URI for the Flask-Limiter instance. Defaults to None.

    Raises:
        RedisError: If an error occurs while connecting to Redis.
        ConfigurationError: If an error occurs while initializing the Flask-Limiter instance.
    """
    app.logger.debug("Initializing the limiter...")
    storage_uri = app.config.get('STORAGE_URL', 'memory://')

    try:
        self._limiter = Limiter(
            key_func=limit_key,
            app=app,
            default_limits=["10 per minute"],
            storage_uri=storage_uri
        )
    except ConfigurationError as e:
        app.logger.error(f"Error initializing the limiter: {e}")
        raise

    if storage_uri.startswith("redis://"):
        try:
            r = redis.Redis.from_url(storage_uri)
            r.ping()
            app.logger.debug("Successfully connected to Redis")
        except RedisError as e:
            app.logger.error(f"Error connecting to Redis: {e}")
            raise

def init_extensions(app):
    """
    Initialize Flask extensions for the given Flask application.

    This function initializes various Flask extensions, including Flask-Compress, Flask-CORS, Flask-Talisman, 
    and Flask-Limiter. It also sets up a function to compress responses after each request.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        None
    """
    initialize_compressor(app)
    #After request for compression
    @app.after_request
    def after_request(response):
        return response_compress(response)
    # Initialize CORS extension
    initialize_cors(app)
    initialize_talisman(app)
    try:
        RateLimiter(app, app.config['STORAGE_URL'])
    except Exception as e:
        app.logger.error(f"Failed to initialize limiter: {e}")

def initialize_compressor(app):
    """
    Initialize the Flask-Compress extension for the given Flask application.

    This function checks if compression is enabled by looking at the 'COMPRESS_ENABLED' configuration item.
    If compression is enabled, it attempts to initialize the Flask-Compress extension and sets up a function
    to compress responses after each request. If an error occurs during initialization, it logs an error message.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        None
    """
    app.logger.debug("Initializing the compressor: %s", app.config.get('COMPRESS_ENABLED', False))
    if app.config.get('COMPRESS_ENABLED', False):
        app.logger.debug("Initializing compression")
        try:
            compress.init_app(app)
            app.after_request(response_compress)
        except Exception as e:
            app.logger.error(f"Failed to initialize compression: {e}")

def response_compress(response):
    """
    Compress the response if it meets certain conditions.

    This function checks if the response should be compressed by calling the `should_compress` function.
    If the response should be compressed, it attempts to compress the response and sets the 'X-Compression-Status' 
    header to 'potential'. If the response should not be compressed, it sets the 'X-Compression-Status' header to 'excluded'.

    Args:
        response (flask.Response): The response object to potentially compress.

    Returns:
        flask.Response: The potentially compressed response object.
    """
    if should_compress(response):
        try:
            response.headers['X-Compression-Status'] = 'potential'
            response = compress.after_request(response)
            return response
        except Exception as e:
            raise
    else:
        response.headers['X-Compression-Status'] = 'excluded'
        return response
    
def initialize_cors(app):
    """
    Initialize the Flask-CORS extension for the given Flask application.
    """
    app.logger.debug("Initializing CORS")
    CORS(app, resources={r"/api/*": {
        "origins": app.config.get("CORS_ORIGINS"), 
        "methods": app.config.get('CORS_METHODS'), 
        "allow_headers": app.config.get('CORS_HEADERS'), 
        "expose_headers": app.config.get('CORS_EXPOSE_HEADERS')}})
    logging.getLogger('flask_cors').level = logging.DEBUG

def initialize_talisman(app):
    """
    Initialize the Flask-Talisman extension for the given Flask application.
    """
    app.logger.debug("Initializing Talisman")
    Talisman(
        app,
        content_security_policy=app.config['TALISMAN_CONTENT_SECURITY_POLICY'],
        force_https=app.config['TALISMAN_FORCE_HTTPS'],
        strict_transport_security=app.config['TALISMAN_STRICT_TRANSPORT_SECURITY'],
        strict_transport_security_preload=app.config['TALISMAN_STRICT_TRANSPORT_SECURITY_PRELOAD'],
        frame_options=app.config['TALISMAN_FRAME_OPTIONS'],
        content_security_policy_nonce_in=app.config['TALISMAN_CONTENT_SECURITY_POLICY_NONCE_IN'],
        referrer_policy=app.config['TALISMAN_REFERRER_POLICY']
    )