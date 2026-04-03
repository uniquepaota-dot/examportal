import os
from django.core.wsgi import get_wsgi_application

# Set settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')

# Run migrations and setup at startup (Hack for Render SQLite)
try:
    import django
    django.setup()
    from django.core.management import call_command
    from django.contrib.auth import get_user_model
    
    print("Running auto-migrations at startup...")
    call_command('migrate', interactive=False)
    
    # Create superuser AFTER migrations
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Default admin created: admin / admin123")
except Exception as e:
    print(f"Startup setup failed: {e}")

application = get_wsgi_application()
