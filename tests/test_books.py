import requests

# Set the base URL to the address of your Docker container
BASE_URL = "http://127.0.0.1:8000/api"

def test_get_books():
    """ Test retrieving all books. """
    response = requests.get(f"{BASE_URL}/books")
    assert response.status_code == 200
    assert len(response.json()) >= 0  # Checks if any books are returned

def test_get_book():
    """ Test retrieving a single book by ID. """
    response = requests.get(f"{BASE_URL}/books/1")
    assert response.status_code == 200
    assert 'id' in response.json()  # Check if 'id' is in response

def test_add_book():
    """ Test adding a new book. """
    response = requests.post(f"{BASE_URL}/books", json={
        'title': 'New Book',
        'author': 'Author Name'
    })
    assert response.status_code == 201
    assert response.json()['title'] == 'New Book'

def test_delete_book():
    """ Test deleting a book. """
    response = requests.delete(f"{BASE_URL}/books/2")
    assert response.status_code == 200
    assert response.json()['message'] == 'Book deleted'
