from django.contrib import admin
from .models import DriverSession, DrowsinessEvent, DetectionLog


@admin.register(DriverSession)
class DriverSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'start_time', 'end_time', 'blink_count', 'drowsy_count', 'total_alerts_triggered')


@admin.register(DrowsinessEvent)
class DrowsinessEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'severity', 'timestamp')


@admin.register(DetectionLog)
class DetectionLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'timestamp')
