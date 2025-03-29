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

# Create an entrypoint script
RUN echo '#!/bin/sh\n\
set -e\n\
\n\
# Wait for database\n\
echo "Waiting for database..."\n\
sleep 5\n\
\n\
# Initialize migrations if not already initialized\n\
if [ ! -d "migrations/versions" ]; then\n\
    echo "Initializing migrations..."\n\
    flask db init\n\
fi\n\
\n\
# Run migrations\n\
echo "Running database migrations..."\n\
flask db stamp head || true\n\
flask db migrate || true\n\
flask db upgrade\n\
\n\
# Start the application\n\
echo "Starting application..."\n\
exec gunicorn --bind 0.0.0.0:5000 "app:app"' > /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

# Expose the port the app runs on
EXPOSE 5000

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"] 