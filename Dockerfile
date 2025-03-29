# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . .

# Create output directory
RUN mkdir -p dist

# Run the crawler
CMD ["python", "crawler.py"] 