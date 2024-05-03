# IP_RANGES: A list of IP ranges for the load balancer.
# These are the IP ranges that the load balancer will accept traffic from.
IP_RANGES = ['35.191.0.0/16', '130.211.0.0/22'] 

# LIMITER_IP_RANGES: A list of IP ranges for the limiter.
# These are the IP ranges that the limiter will apply limits to.
LIMITER_IP_RANGES = ['35.191.0.0/16', '130.211.0.0/22'] 


# COMPRESSION SETTINGS
# COMPRESS_ENABLED: Whether to enable compression.
COMPRESS_ENABLED = True

# COMPRESS_REGISTER: Whether to register the extension with the Flask app.
# If this is False, the extension will not be registered with the Flask app. Compression will be applied to a response only if the response is marked for compression.
COMPRESS_REGISTER = False

# COMPRESS_EXCLUDE: A list of paths to exclude from compression.
# These are the paths that will not be compressed by the Flask-Compress extension.
COMPRESS_EXCLUDE = ['/static/', '/favicon.ico', '/api/large-data-no-compress']

# COMPRESS_MIMETYPES: A list of MIME types to compress.
# These are the MIME types that the Flask-Compress extension will compress.
COMPRESS_MIMETYPES = ['application/javascript',
                      'application/json',
                      'text/css',
                      'text/html',
                      'text/javascript',
                      'text/xml',]

# COMPRESS_LEVEL: The level of compression to apply, from 0 (no compression) to 9 (maximum compression).
# This is the level of compression that the Flask-Compress extension will apply.
COMPRESS_LEVEL = 6

# COMPRESS_MIN_SIZE: The minimum size in bytes for a response to be compressed.
# This is the minimum size of a response that the Flask-Compress extension will compress.
COMPRESS_MIN_SIZE = 500

# COMPRESS_ALGORITHM: The compression algorithm to use.
# This is the compression algorithm that the Flask-Compress extension will use.
COMPRESS_ALGORITHM = 'gzip'



# CORS settings
# CORS_ORIGINS: A list of origins that are allowed to make cross-origin requests.
# "*" means that all origins are allowed. In a production environment, you should
# limit this to the domains that should have access to your API.
CORS_ORIGINS = ["*"]

# CORS_METHODS: A list of HTTP methods that are allowed for cross-origin requests.
# In this case, GET, POST, PUT, and DELETE requests are allowed.
CORS_METHODS = ["GET", "POST", "PUT", "DELETE"]

# CORS_HEADERS: A list of HTTP headers that are allowed in cross-origin requests.
# In this case, the Content-Type and Authorization headers are allowed.
CORS_HEADERS = ["Content-Type", "Authorization"]

# CORS_EXPOSE_HEADERS: A list of HTTP headers that are allowed to be exposed to the browser.
# In this case, the Content-Type and Authorization headers are allowed to be exposed.
CORS_EXPOSE_HEADERS = ["Content-Type", "Authorization"]


# Flask-Talisman settings
# TALISMAN_CONTENT_SECURITY_POLICY: The Content Security Policy to be used by Flask-Talisman.
# This is the Content Security Policy that Flask-Talisman will enforce.
TALISMAN_CONTENT_SECURITY_POLICY = None

# TALISMAN_FORCE_HTTPS: Whether Flask-Talisman should force HTTPS.
# If this is True, Flask-Talisman will redirect all HTTP requests to HTTPS.
TALISMAN_FORCE_HTTPS = False

# TALISMAN_STRICT_TRANSPORT_SECURITY: Whether Flask-Talisman should use Strict Transport Security.
# If this is True, Flask-Talisman will include the Strict-Transport-Security header in responses.
TALISMAN_STRICT_TRANSPORT_SECURITY = False

# TALISMAN_STRICT_TRANSPORT_SECURITY_PRELOAD: Whether Flask-Talisman should use Strict Transport Security preload.
# If this is True, Flask-Talisman will include the preload directive in the Strict-Transport-Security header.
TALISMAN_STRICT_TRANSPORT_SECURITY_PRELOAD = True

# TALISMAN_FRAME_OPTIONS: The frame options to be used by Flask-Talisman.
# This is the value of the X-Frame-Options header that Flask-Talisman will include in responses.
TALISMAN_FRAME_OPTIONS = 'DENY'

# TALISMAN_CONTENT_SECURITY_POLICY_NONCE_IN: The Content Security Policy nonce to be used by Flask-Talisman.
# This is the nonce that Flask-Talisman will include in the script-src directive of the Content Security Policy.
TALISMAN_CONTENT_SECURITY_POLICY_NONCE_IN = ['script-src']

# TALISMAN_REFERRER_POLICY: The referrer policy to be used by Flask-Talisman.
# This is the value of the Referrer-Policy header that Flask-Talisman will include in responses.
TALISMAN_REFERRER_POLICY = 'strict-origin-when-cross-origin'


# Other configuration settings...
