from functools import wraps
import ipaddress
import os
from flask import abort, request, current_app, has_request_context
from ipaddress import ip_address

def init_valid_routes(app):
    """
    Initialize the 'VALID_ROUTES' configuration item with all valid routes and their methods.

    This function iterates over all routes defined in the Flask application, excluding static routes.
    For each route, it adds the route and its methods to the 'VALID_ROUTES' configuration item.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        None
    """
    # Initialize valid_routes after all routes are defined
    app.config['VALID_ROUTES'] = {}
    for rule in app.url_map.iter_rules():
        if not rule.rule.startswith('/static'):  # Exclude all static routes
            if str(rule) not in app.config['VALID_ROUTES']:
                app.config['VALID_ROUTES'][str(rule)] = list(rule.methods)
            else:
                app.config['VALID_ROUTES'][str(rule)].extend([method for method in rule.methods if method not in app.config['VALID_ROUTES'][str(rule)]])
    
    app.logger.debug(f"Valid routes: {app.config['VALID_ROUTES']}")

def should_compress(response):
    """
    Determine whether to compress the response based on specific conditions.
    
    Considerations for compressing responses:
    - **Direct Passthrough**: Do not compress if the response is marked with direct_passthrough, typically used for streaming large data.
    - **Sensitive Data**: Avoid compressing sensitive data to mitigate risks such as security vulnerabilities like the BREACH attack.
    - **Response Size**: Skip compression for very small responses where the overhead does not justify the benefits.
    - **Performance**: Consider the additional CPU load due to compression, especially under high traffic.
    - **Content Type**: Certain content types like already compressed files (e.g., JPEG, PNG, ZIP) do not benefit from further compression.
    

    Args:
        response (flask.Response): The response object to potentially compress.

    Returns:
        bool: True if the response should be compressed, False otherwise.
    """
    if response.direct_passthrough:
        return False
    path = request.path.rstrip('/')
    if path in current_app.config.get('COMPRESS_EXCLUDE', []):
        return False
    if len(response.get_data(as_text=False)) < current_app.config.get('COMPRESS_MIN_SIZE', 500):
        return False
    if response.mimetype not in current_app.config.get('COMPRESS_MIMETYPES', []):
        return False
    return True


def limit_key():
    """
    Determine the rate limiting key based on the request's IP address.
    Allows unlimited access from specified IP ranges.
    
    Returns:
        str: 'unlimited' if the IP address is within the allowed range, otherwise the IP address.
    """
    # Ensure the function is called in a request context
    if not has_request_context():
        raise RuntimeError("limit_key function called outside of request context")

    remote_addr = request.remote_addr
    if 'LIMITER_IP_RANGES' in current_app.config:
        try:
            ip = ipaddress.ip_address(remote_addr)
            for ip_range in current_app.config['LIMITER_IP_RANGES']:
                if ip in ip_range:
                    return 'unlimited'
        except ValueError:
            current_app.logger.error(f"Invalid IP address received: {remote_addr}")
            return None  # or handle as appropriate

    return remote_addr

def get_env_variable(var_name):
    """
    Get the environment variable or return exception.

    Args:
        var_name (str): The name of the environment variable to get.

    Returns:
        str: The value of the environment variable.

    Raises:
        Exception: If the environment variable is not set.
    """
    try:
        return os.environ[var_name]
    except KeyError:
        error_message = f"{var_name} environment variable is not set."
        current_app.logger.error(error_message)
        raise Exception(error_message)

def str_to_bool(s):
    """
    Convert a string to a boolean.

    Args:
        s (str): The string to convert.

    Returns:
        bool: The boolean representation of the string.
    """
    return s.lower() in ['true', '1', 't', 'y', 'yes']

def check_ip():
    """
    Check if the incoming request IP address falls within any of the IP ranges.

    Returns:
        bool: True if the IP address is in the range, False otherwise.
    """
    # Return False if 'IP_RANGES' is not in the configuration
    if 'IP_RANGES' not in current_app.config:
        return False

    ip = ip_address(request.remote_addr)  # Get the IP address of the incoming request

    # Check if the IP address is in any of the IP ranges
    return any(ip in ip_range for ip_range in current_app.config['IP_RANGES'])

def skip_for_health_checks(f):
    """
    Decorator function to skip the decorated function for Health Checks.

    Args:
        f (function): The function to decorate.

    Returns:
        function: The decorated function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.path == current_app.config.get('HEALTH_CHECK_ROUTE', "/") and request.method == "GET":
            return f(*args, **kwargs)  # Continue with the function for this specific route and method
        
        if request.user_agent.string == current_app.config.get('HEALTH_CHECK_USER_AGENT', "") and check_ip():
            return  # Skip the function for Health Checks
        return f(*args, **kwargs)
    return decorated_function

@skip_for_health_checks
def validate_route_and_method():
    """
    Before request handler to validate the requested route and method.

    This function is intended to be used as a before request handler in a Flask application.
    It checks if the requested route and method are valid according to the application's configuration.
    If the route is not valid, it aborts the request with a 404 status code.
    If the method is not allowed for the route, it aborts the request with a 405 status code and logs a warning.

    This function should be decorated with @skip_for_health_checks to ensure that it does not interfere with health checks.
    """
    valid_routes = current_app.config['VALID_ROUTES']

    # Check if the path is valid
    if str(request.url_rule) not in valid_routes:
        abort(404)  # Not found

    # Check if the method is allowed for the path
    allowed_methods = valid_routes.get(str(request.url_rule))
    if request.method not in allowed_methods:
        current_app.logger.warning(f"Method {request.method} not allowed for path {request.url_rule}. Allowed methods: {allowed_methods}")
        abort(405)  # Method not allowed

def handle_internal_server_error(e):
    """
    Handle 500 errors which are not caught by other handlers.

    This function logs the error and returns a JSON response with a message
    indicating an internal server error and a 500 status code.

    Parameters:
    e (Exception): The exception that caused the 500 error.

    Returns:
    tuple: A tuple containing a dictionary with a message and a 500 status code.
    """
    current_app.logger.error("An unexpected 500 error occurred: %s", e)
    return {"message": "Internal server error, please try again later."}, 500

def handle_not_found_error(e):
    """
    Handle 404 errors which are not caught by other handlers.

    This is an exceptional situation as these errors are usually handled elsewhere.
    This function logs the error and returns a JSON response with a message
    indicating a not found error and a 404 status code.

    Parameters:
    e (Exception): The exception that caused the 404 error.

    Returns:
    tuple: A tuple containing a dictionary with a message and a 404 status code.
    """
    current_app.logger.error("An unexpected 404 error occurred: %s", e)
    return {"message": "The requested resource could not be found."}, 404

def handle_method_not_allowed_error(e):
    """
    Handle 405 errors which are not caught by other handlers.

    This is an exceptional situation as these errors are usually handled elsewhere.
    This function logs the error and returns a JSON response with a message
    indicating a method not allowed error and a 405 status code.

    Parameters:
    e (Exception): The exception that caused the 405 error.

    Returns:
    tuple: A tuple containing a dictionary with a message and a 405 status code.
    """
    current_app.logger.error("An unexpected 405 error occurred: %s", e)
    return {"message": "The requested method is not allowed for this resource."}, 405