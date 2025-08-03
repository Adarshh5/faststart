from django.apps import AppConfig
# import user_data.signals as signals 

class UserDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user_data'
    def ready(self):
        # Import signals to ensure they are registered
       import apps.user_data.signals  # Assuming signals.py is in the same app
