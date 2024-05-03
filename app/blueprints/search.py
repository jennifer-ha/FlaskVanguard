from urllib import response
from flask import Blueprint, jsonify
#from app.extensions import limiter

search = Blueprint('search', __name__)

@search.route('/books/search', methods=['GET'])
#@limiter.limiter.limit("5 per minute")
def search_books():

    # Your existing search logic
    return jsonify({"message": "Search completed"}), 200

@search.route('/books/search_default_limit', methods=['GET'])
def search_books_default_limit():
    # Your existing search logic
    return jsonify({"message": "Search completed"}), 200

@search.route("/large-data")
def large_data():
    """ Return a large amount of data. """
    data = "x" * 1000000  # 1 million characters
    return jsonify(data=data)

@search.route("/large-data-no-compress")
def large_data_no_compress():
    """ Return a large amount of data. """
    response.direct_passthrough = True
    data = "x" * 1000000  # 1 million characters
    return jsonify(data=data)
