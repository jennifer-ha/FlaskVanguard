import ipaddress
import os
from app.utils import get_env_variable


def configure_app(app, is_production):
    """
    Configure the Flask application based on the production flag.

    This function sets various configuration items for the Flask application, 
    such as compression settings, IP ranges, CORS settings, Flask-Talisman settings, 
    and the limiter storage URI. The specific settings depend on whether the application 
    is running in production mode or not.

    Args:
        app (Flask): The Flask application instance.
        is_production (bool): A flag indicating whether the application is running in production mode.

    Returns:
        None
    """
    if is_production == True:
        from .prod_config import COMPRESS_ENABLED, COMPRESS_REGISTER, COMPRESS_MIMETYPES, COMPRESS_LEVEL, COMPRESS_MIN_SIZE, COMPRESS_ALGORITHM, IP_RANGES, LIMITER_IP_RANGES, CORS_ORIGINS, CORS_METHODS, CORS_HEADERS, CORS_EXPOSE_HEADERS, TALISMAN_CONTENT_SECURITY_POLICY, TALISMAN_FORCE_HTTPS, TALISMAN_STRICT_TRANSPORT_SECURITY, TALISMAN_STRICT_TRANSPORT_SECURITY_PRELOAD, TALISMAN_FRAME_OPTIONS, TALISMAN_CONTENT_SECURITY_POLICY_NONCE_IN, TALISMAN_REFERRER_POLICY, COMPRESS_EXCLUDE
        # Load Production config if passed in
        app.config['TEST_MODE'] = False
        test_config = {}
        app.config.update(test_config)

        # Set configuration settings
        app.config['COMPRESS_ENABLED'] = COMPRESS_ENABLED
        app.config['COMPRESS_REGISTER'] = COMPRESS_REGISTER  
        app.config['COMPRESS_MIMETYPES'] = COMPRESS_MIMETYPES
        app.config['COMPRESS_LEVEL'] = COMPRESS_LEVEL
        app.config['COMPRESS_MIN_SIZE'] = COMPRESS_MIN_SIZE
        app.config['COMPRESS_ALGORITHM'] = COMPRESS_ALGORITHM
        app.config['IP_RANGES'] = IP_RANGES
        app.config['LIMITER_IP_RANGES'] = [ipaddress.ip_network(ip) for ip in LIMITER_IP_RANGES]
        # CORS settings
        app.config['CORS_ORIGINS'] = CORS_ORIGINS
        app.config['CORS_METHODS'] = CORS_METHODS
        app.config['CORS_HEADERS'] = CORS_HEADERS
        app.config['CORS_EXPOSE_HEADERS'] = CORS_EXPOSE_HEADERS
        # Flask-Talisman settings
        app.config['TALISMAN_CONTENT_SECURITY_POLICY'] = TALISMAN_CONTENT_SECURITY_POLICY
        app.config['TALISMAN_FORCE_HTTPS'] = TALISMAN_FORCE_HTTPS
        app.config['TALISMAN_STRICT_TRANSPORT_SECURITY'] = TALISMAN_STRICT_TRANSPORT_SECURITY
        app.config['TALISMAN_STRICT_TRANSPORT_SECURITY_PRELOAD'] = TALISMAN_STRICT_TRANSPORT_SECURITY_PRELOAD
        app.config['TALISMAN_FRAME_OPTIONS'] = TALISMAN_FRAME_OPTIONS
        app.config['TALISMAN_CONTENT_SECURITY_POLICY_NONCE_IN'] = TALISMAN_CONTENT_SECURITY_POLICY_NONCE_IN
        app.config['TALISMAN_REFERRER_POLICY'] = TALISMAN_REFERRER_POLICY
        
        # Set the limiter storage URI depending on the environment
        app.logger.debug("Running in production mode. Limiter storage URI set to Redis://redis:6379/0")
        app.config['REDIS_PASSWORD'] = os.getenv("REDIS_PASSWORD", "empty").strip("'").strip()
        if app.config['REDIS_PASSWORD'] == "empty":
            app.logger.error("REDIS_PASSWORD environment variable is not set")
            raise Exception("REDIS_PASSWORD environment variable is not set")
        app.config['STORAGE_URL'] = f"redis://:{app.config['REDIS_PASSWORD']}@redis:6379/0"
        app.config['COMPRESS_EXCLUDE'] = COMPRESS_EXCLUDE
    else:
        # Test or development configuration
        from .test_config import COMPRESS_ENABLED, COMPRESS_REGISTER, COMPRESS_MIMETYPES, COMPRESS_LEVEL, COMPRESS_MIN_SIZE, COMPRESS_ALGORITHM, IP_RANGES, LIMITER_IP_RANGES, CORS_ORIGINS, CORS_METHODS, CORS_HEADERS, CORS_EXPOSE_HEADERS, TALISMAN_CONTENT_SECURITY_POLICY, TALISMAN_FORCE_HTTPS, TALISMAN_STRICT_TRANSPORT_SECURITY, TALISMAN_STRICT_TRANSPORT_SECURITY_PRELOAD, TALISMAN_FRAME_OPTIONS, TALISMAN_CONTENT_SECURITY_POLICY_NONCE_IN, TALISMAN_REFERRER_POLICY, COMPRESS_EXCLUDE
        app.config['TEST_MODE'] = True
        from dotenv import load_dotenv
        load_dotenv()
        app.config['SECRET_KEY'] = get_env_variable('SECRET_KEY').strip("'").strip()

        # Set configuration settings
        app.config['COMPRESS_ENABLED'] = COMPRESS_ENABLED
        app.config['COMPRESS_REGISTER'] = COMPRESS_REGISTER  
        app.config['COMPRESS_MIMETYPES'] = COMPRESS_MIMETYPES
        app.config['COMPRESS_LEVEL'] = COMPRESS_LEVEL
        app.config['COMPRESS_MIN_SIZE'] = COMPRESS_MIN_SIZE
        app.config['COMPRESS_ALGORITHM'] = COMPRESS_ALGORITHM
        app.config['IP_RANGES'] = IP_RANGES
        app.config['LIMITER_IP_RANGES'] = [ipaddress.ip_network(ip) for ip in LIMITER_IP_RANGES]
        app.config['CORS_ORIGINS'] = CORS_ORIGINS
        app.config['CORS_METHODS'] = CORS_METHODS
        app.config['CORS_HEADERS'] = CORS_HEADERS
        app.config['CORS_EXPOSE_HEADERS'] = CORS_EXPOSE_HEADERS
        # Flask-Talisman settings
        app.config['TALISMAN_CONTENT_SECURITY_POLICY'] = TALISMAN_CONTENT_SECURITY_POLICY
        app.config['TALISMAN_FORCE_HTTPS'] = TALISMAN_FORCE_HTTPS
        app.config['TALISMAN_STRICT_TRANSPORT_SECURITY'] = TALISMAN_STRICT_TRANSPORT_SECURITY
        app.config['TALISMAN_STRICT_TRANSPORT_SECURITY_PRELOAD'] = TALISMAN_STRICT_TRANSPORT_SECURITY_PRELOAD
        app.config['TALISMAN_FRAME_OPTIONS'] = TALISMAN_FRAME_OPTIONS
        app.config['TALISMAN_CONTENT_SECURITY_POLICY_NONCE_IN'] = TALISMAN_CONTENT_SECURITY_POLICY_NONCE_IN
        app.config['TALISMAN_REFERRER_POLICY'] = TALISMAN_REFERRER_POLICY
        
        # Set the limiter storage URI depending on the environment
        app.logger.debug("Running in test mode. Limiter storage URI set to memory://")
        app.config['STORAGE_URL'] = "memory://"
        app.config['COMPRESS_EXCLUDE'] = COMPRESS_EXCLUDE
