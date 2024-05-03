import os
from app import create_app

app = create_app(os.getenv('PRODUCTION') == 'true')

if __name__ == "__main__":
    app.run()
