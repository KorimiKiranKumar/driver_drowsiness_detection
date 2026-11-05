from django.db import models
from django.conf import settings
from apps.detection.models import DriverSession

User = settings.AUTH_USER_MODEL


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(DriverSession, on_delete=models.CASCADE)
    total_events = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report - {self.user}"