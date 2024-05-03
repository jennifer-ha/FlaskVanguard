from flask import Flask, request, Response, current_app
from flask_compress import Compress
from werkzeug.wrappers import Response as WerkzeugResponse

class CompressMiddleware:
    def __init__(self, app, compress, config):
        self.app = app
        self.compress = compress
        self.config = config 

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            return start_response(status, headers, exc_info)

        # Creëer een proxy response object
        response = WerkzeugResponse.from_app(self.app, environ)

        # Haal de path informatie veilig uit het environment
        path = environ.get('PATH_INFO', '')

        # Controleer de compressievoorwaarden
        if self.should_compress(response, path):
            # Gebruik de compress middleware als het moet
            return self.compress.app(environ, start_response)
        else:
            # Bypass compressie als het niet moet
            return self.app(environ, start_response)

    def should_compress(self, response, path):
        if response.direct_passthrough:
            return False
        if path.rstrip('/') in current_app.config.get('COMPRESS_EXCLUDE', []):
            return False
        if len(response.get_data(as_text=True)) < current_app.config.get('COMPRESS_MIN_SIZE', 500):
            return False
        if response.mimetype not in current_app.config.get('COMPRESS_MIMETYPES', []):
            return False
        return True

