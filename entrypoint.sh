#!/bin/bash

echo "Waiting for DB to be ready..."
# Wait for DB to be ready (optional, you can improve this)
sleep 5

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000
