# Use an official Python runtime as the parent image for the build stage
FROM python:3.12-slim as build

# Set the working directory in the container
WORKDIR /app

# Update the system and install security updates in one layer, then clean up
RUN apt-get update && apt-get upgrade -y && \
    apt-get dist-upgrade -y && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy only the requirements file and the WSGI entry point file
COPY requirements.txt .
COPY wsgi.py .

# Create and activate a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install required packages in one layer
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code and the Gunicorn configuration
COPY app/. /app/app/
COPY gunicorn_config.py .

# Start a new, final stage
FROM python:3.12-slim

WORKDIR /app

COPY --from=build /app /app
COPY --from=build /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# Create a non-root user and switch to it
RUN useradd --create-home appuser
RUN chown -R appuser:appuser /app 
USER appuser

# Expose the port for the Flask app
EXPOSE 8000

# Start the app with Gunicorn
CMD ["gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]
