#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Run migrations during build
echo "--> Running migrations during build..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
