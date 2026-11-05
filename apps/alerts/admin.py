from django.contrib import admin
from .models import Alert, AlertPreference, AlertHistory


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'created_at')


@admin.register(AlertPreference)
class AlertPreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'visual_enabled', 'audio_enabled', 'sms_enabled', 'email_enabled')


@admin.register(AlertHistory)
class AlertHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session', 'alert_type', 'severity', 'message', 'timestamp', 'acknowledged')
