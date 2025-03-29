#!/bin/sh
set -e

echo "Waiting for database..."
sleep 5

if [ ! -d "migrations/versions" ]; then
    echo "Initializing migrations..."
    flask db init
fi

echo "Running database migrations..."
flask db stamp head || true
flask db migrate || true
flask db upgrade

echo "Starting application..."
exec gunicorn --bind 0.0.0.0:5000 "app:app" 