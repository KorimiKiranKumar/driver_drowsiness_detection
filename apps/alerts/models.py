from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class AlertPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    visual_enabled = models.BooleanField(default=True)
    audio_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    email_enabled = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    # New preference fields
    sound_volume = models.IntegerField(default=80)
    sound_type = models.CharField(max_length=20, default='beep')
    visual_intensity = models.CharField(max_length=20, default='medium')
    visual_color = models.CharField(max_length=20, default='red')
    drowsiness_threshold = models.IntegerField(default=70)
    alert_delay = models.IntegerField(default=3)

    def __str__(self):
        return f"Alert Preference for {self.user}"


class AlertHistory(models.Model):
    ALERT_TYPE_CHOICES = [
        ('VISUAL', 'Visual'),
        ('AUDIO', 'Audio'),
        ('SMS', 'SMS'),
        ('EMAIL', 'Email')
    ]

    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey('detection.DriverSession', on_delete=models.SET_NULL, null=True, blank=True)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES, default='VISUAL')
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='LOW')
    message = models.CharField(max_length=255)
    ear = models.FloatField(null=True, blank=True)
    mar = models.FloatField(null=True, blank=True)
    head_pose = models.CharField(max_length=20, null=True, blank=True)
    acknowledged = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alert_type} ({self.severity}) for {self.user} @ {self.timestamp}"
