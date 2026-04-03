#!/usr/bin/env bash
# exit on error
set -o errexit

# Run Migrations
echo "--> Running migrations..."
python manage.py migrate --noinput || { echo "!! Migration failed"; exit 1; }

# Create Superuser (admin / admin123)
echo "--> Creating superuser if it doesn't exist..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell

# Start Gunicorn
echo "--> Starting Gunicorn..."
gunicorn exam_portal.wsgi:application

