from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class DriverSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    blink_count = models.IntegerField(default=0)
    drowsy_count = models.IntegerField(default=0)
    total_alerts_triggered = models.IntegerField(default=0)
    
    # Head Pose Tracking
    head_straight_count = models.IntegerField(default=0)
    head_up_count = models.IntegerField(default=0)
    head_down_count = models.IntegerField(default=0)
    head_left_count = models.IntegerField(default=0)
    head_right_count = models.IntegerField(default=0)
    total_frames = models.IntegerField(default=0)

    def __str__(self):
        user_display = self.user.username if self.user else "Anonymous"
        return f"{user_display} - {self.start_time}"

    @property
    def duration(self):
        if self.start_time is None:
            return 0
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (timezone.now() - self.start_time).total_seconds()

    @property
    def total_frames_processed(self):
        # Fall back to number of logged events if we don't have explicit frame count.
        return self.drowsinessevent_set.count() + self.blink_count

    @property
    def total_drowsy_events(self):
        return self.drowsinessevent_set.filter(severity__in=['DROWSY', 'HIGH', 'MEDIUM']).count()

    @property
    def status(self):
        return 'COMPLETED' if self.end_time else 'ACTIVE'


class DrowsinessEvent(models.Model):
    session = models.ForeignKey(DriverSession, on_delete=models.CASCADE)
    severity = models.CharField(max_length=20)
    ear = models.FloatField(null=True, blank=True)
    mar = models.FloatField(null=True, blank=True)
    head_pose = models.CharField(max_length=20, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session.user} - {self.severity} @ {self.timestamp}"


class DetectionLog(models.Model):
    """Log for detection events (used by WebSocket consumer)."""
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.status} @ {self.timestamp}"
