# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app/__init__.py
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

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

# Create migrations directory if it doesn't exist
RUN mkdir -p migrations

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh

# Expose the port the app runs on
EXPOSE 5000

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"] 