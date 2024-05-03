from flask import Flask
from app.config_app import configure_app
from app.logging_config import configure_logging
from .extensions import  init_extensions
from .register_blueprints import register_blueprints

# Import your utilities and configuration settings
from .utils import init_valid_routes, validate_route_and_method, handle_internal_server_error, handle_not_found_error, handle_method_not_allowed_error

def create_app(is_production):


    app = Flask(__name__, static_url_path='/static')

    configure_app(app, is_production)
    configure_logging(app)
    app.logger.critical("TEST_MODE: %s", app.config['TEST_MODE'])
    init_extensions(app)
    register_blueprints(app)
    init_valid_routes(app)

    # Register error handlers
    app.register_error_handler(500, handle_internal_server_error)
    app.register_error_handler(404, handle_not_found_error)
    app.register_error_handler(405, handle_method_not_allowed_error)

    # Register before_request handler
    app.before_request(validate_route_and_method)

    return app


