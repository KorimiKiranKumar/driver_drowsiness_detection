"""
Detection App Configuration
"""

from django.apps import AppConfig


class DetectionConfig(AppConfig):
    """Detection app configuration."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.detection'
    verbose_name = 'Detection'
    
    def ready(self):
        """Import signals when app is ready."""
        pass
