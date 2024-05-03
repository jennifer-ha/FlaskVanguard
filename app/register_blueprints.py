# register_blueprints.py
from app.blueprints.books import books
from app.blueprints.search import search

def register_blueprints(app):
    app.register_blueprint(books, url_prefix='/api')
    app.register_blueprint(search, url_prefix='/api')