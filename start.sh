#!/usr/bin/env bash
# exit on error
set -o errexit

# Run Migrations
python manage.py migrate --noinput

# Create Superuser (admin / admin123)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell

# Start Gunicorn
gunicorn exam_portal.wsgi:application
