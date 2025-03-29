# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for psycopg2 and curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . .

# Make sure the app directory is in the Python path
ENV PYTHONPATH=/app

# Create migrations directory if it doesn't exist
RUN mkdir -p migrations

# Expose the port the app runs on
EXPOSE 5000

# Command to run migrations and start the application
CMD flask db upgrade && gunicorn --bind 0.0.0.0:5000 'app:app' 