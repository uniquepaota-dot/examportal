from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # Create superuser at startup if not exists
        import os
        # We use a simple check to ensure this only runs once in the main process
        if os.environ.get('RUN_MAIN') != 'true': 
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                if not User.objects.filter(username='admin').exists():
                    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
                    print("Default admin created: admin / admin123")
            except Exception as e:
                print(f"Superuser creation skipped or failed: {e}")
