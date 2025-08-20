#!/bin/bash
set -e

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files (noinput to avoid prompts)
python manage.py collectstatic --noinput

# Run create_groups to set up permissions
python manage.py create_groups

# Run the command (passed from docker-compose)
exec "$@"