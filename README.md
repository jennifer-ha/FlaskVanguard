# FlaskVanguard-Boilerplate

Welcome to FlaskVanguard-Boilerplate, a cutting-edge, scalable framework designed for building high-performance web applications with Flask. This boilerplate integrates advanced security measures, efficient rate limiting, and robust logging capabilities, offering a comprehensive foundation for enterprise-level projects.

## Key Features

- **Advanced Security:** Comes pre-configured with Flask-Talisman and CORS to secure your application against common vulnerabilities.
- **Rate Limiting:** Manage and mitigate traffic effectively to prevent overloads and ensure seamless operation during peak loads.
- **Modular Design:** Utilizes Flask Blueprints to organize your application into distinct components, making it easier to maintain and scale.
- **Production-Ready:** Includes Dockerfiles for both development and production to streamline deployment processes.
- **Logging and Monitoring:** Implements a sophisticated logging system to aid in monitoring and diagnosing issues in real-time.

## Getting Started

Follow these steps to set up and run FlaskVanguard-Boilerplate on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6 or higher
- Docker
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jennifer-ha/FlaskVanguard.git
   cd FlaskVanguard

2. **Set up a virtual environment**
    ```bash
    python -m venv venv 
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt

4. **Run the application**
    ```bash
    gunicorn wsgi:app

5. **Visit/test the application**
    - Open your web browser and go to http://127.0.0.1:5000/api/books to see the application in action.
    - curl http://127.0.0.1:5000/api/books

    - Go to the tests folder
    - Change BASE_URL = "http://127.0.0.1:8000/api" to BASE_URL = "http://127.0.0.1:5000/api" in test_search.py and test_books.py
    

### Docker Setup

## Development / Testing Environment

To run the application in a Docker container for development or testing, follow these steps:

1. **Build and run the Docker environment**
   ```bash
   docker-compose up --build
   
2.  **Stopping Docker Containers**
To stop and remove all containers, networks, and volumes created by Docker Compose, you can use the following command:
    ```bash
    docker-compose down

## Production Environment

For deploying the application in a production environment, use the production-specific Docker Compose file:

1. **Build and run the Docker environment for production**
    ```bash
    docker-compose -f docker-compose.prod.yml up --build

2. **Stopping Docker Containers**
    ```bash
    docker-compose -f docker-compose.prod.yml down

### Testing

run test in the test folder
    ```bash
    cd tests
    pytest

### Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request

### License

Distributed under the MIT License. See LICENSE for more information.

