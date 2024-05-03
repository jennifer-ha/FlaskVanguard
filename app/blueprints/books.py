from flask import current_app, request, jsonify, Blueprint


# Mock data for the books
book_data = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}
]

#Create a Blueprint Instance
books = Blueprint('books', __name__)

# Route to get all books
@books.route('/books', methods=['GET'])
def get_books():
    return jsonify(book_data)

# Route to get a specific book by ID
@books.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in book_data if book['id'] == book_id), None)
    if book is not None:
        return jsonify(book)
    else:
        current_app.logger.warning(f"Book with ID {book_id} not found")
        return {"message": "Book not found"}, 404

# Route to add a new book
# Route to add a book
@books.route('/books', methods=['POST'])
def add_book():
    if not request.json or 'title' not in request.json or 'author' not in request.json:
        current_app.logger.warning("Invalid data")
        return {"message": "Invalid data"}, 400
    book = {
        'id': book_data[-1]['id'] + 1,
        'title': request.json['title'],
        'author': request.json['author']
    }
    book_data.append(book)
    return jsonify(book), 201

# Route to delete a book
@books.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global book_data
    book_data = [book for book in book_data if book['id'] != book_id]
    return {"message": "Book deleted"}, 200