"""
Reports App Configuration
"""

from django.apps import AppConfig


class ReportsConfig(AppConfig):
    """Reports app configuration."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.reports'
    verbose_name = 'Reports'
    
    def ready(self):
        """Import signals when app is ready."""
        pass
