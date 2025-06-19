"""
Django app configuration for chart management app.
"""

from django.apps import AppConfig


class ChartManagementConfig(AppConfig):
    """Configuration for the chart management app"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.chart_management"
    verbose_name = "Chart Management"

    def ready(self):
        """App ready signal handler"""
        # Import signals to ensure they are registered
        from . import signals
