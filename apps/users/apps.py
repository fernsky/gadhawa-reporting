"""
Users app configuration
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = 'प्रयोगकर्ता व्यवस्थापन'  # User Management in Nepali
    
    def ready(self):
        """
        Import signals when the app is ready
        """
        try:
            import apps.users.signals  # noqa F401
        except ImportError:
            pass
