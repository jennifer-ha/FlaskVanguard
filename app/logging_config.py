import logging
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    """Configure app logging."""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG if app.config['TEST_MODE'] else logging.ERROR)
    app.logger.propagate = False
