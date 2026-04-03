"""
WSGI config for exam_portal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Run migrations at startup (Hack for Render SQLite)
try:
    import django
    from django.core.management import call_command
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
    django.setup()
    print("Running auto-migrations...")
    call_command('migrate', interactive=False)
except Exception as e:
    print(f"Startup migration failed: {e}")

application = get_wsgi_application()
