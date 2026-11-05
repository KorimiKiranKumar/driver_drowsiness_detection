"""
Alerts Services
Handles alert generation and notification delivery.
"""

import winsound
import threading
from django.utils import timezone
from .models import AlertHistory, AlertPreference


class AlertService:
    """Service for managing alerts and notifications."""
    
    def __init__(self, user, session):
        """
        Initialize alert service.
        
        Args:
            user: User instance
            session: DriverSession instance
        """
        self.user = user
        self.session = session
        self.preferences = self._get_preferences()
    
    def _get_preferences(self):
        """Get user alert preferences."""
        try:
            return AlertPreference.objects.get(user=self.user)
        except AlertPreference.DoesNotExist:
            # Create default preferences
            return AlertPreference.objects.create(user=self.user)
    
    def trigger_alert(self, severity, message, ear_value, mar_value, head_pose):
        """
        Trigger alert based on severity and user preferences.
        
        Args:
            severity: Alert severity (LOW, MEDIUM, HIGH)
            message: Alert message
            ear_value: Eye Aspect Ratio value
            mar_value: Mouth Aspect Ratio value
            head_pose: Head pose category
        """
        # Always trigger visual alert
        if self.preferences.visual_enabled:
            self._create_alert_history('VISUAL', severity, message, ear_value, mar_value, head_pose)
        
        # Trigger audio alert
        if self.preferences.audio_enabled:
            self._trigger_audio_alert(severity)
            self._create_alert_history('AUDIO', severity, message, ear_value, mar_value, head_pose)
        
        # Trigger SMS alert for HIGH severity
        if severity == 'HIGH' and self.preferences.sms_enabled and self.preferences.phone_number:
            self._trigger_sms_alert(message)
            self._create_alert_history('SMS', severity, message, ear_value, mar_value, head_pose)
        
        # Trigger email alert for HIGH severity
        if severity == 'HIGH' and self.preferences.email_enabled and self.preferences.email:
            self._trigger_email_alert(message)
            self._create_alert_history('EMAIL', severity, message, ear_value, mar_value, head_pose)
        
        # Update session statistics
        self.session.total_alerts_triggered += 1
        self.session.save()
    
    def _create_alert_history(self, alert_type, severity, message, ear_value=None, mar_value=None, head_pose=None):
        """Create alert history record."""
        AlertHistory.objects.create(
            user=self.user,
            session=self.session,
            alert_type=alert_type,
            severity=severity,
            message=message,
            ear=ear_value,
            mar=mar_value,
            head_pose=head_pose
        )
    
    def _trigger_audio_alert(self, severity):
        """Trigger audio alert."""
        try:
            if severity == 'HIGH':
                # Play urgent beep
                threading.Thread(target=self._play_urgent_beep, daemon=True).start()
            else:
                # Play normal beep
                threading.Thread(target=self._play_normal_beep, daemon=True).start()
        except Exception as e:
            print(f"Error triggering audio alert: {e}")
    
    def _play_urgent_beep(self):
        """Play urgent beep sound."""
        try:
            for _ in range(3):
                winsound.Beep(1000, 300)
                winsound.Beep(1500, 300)
        except Exception:
            print('\a\a\a')  # Fallback to ASCII bell
    
    def _play_normal_beep(self):
        """Play normal beep sound."""
        try:
            winsound.Beep(1000, 500)
        except Exception:
            print('\a')  # Fallback to ASCII bell
    
    def _trigger_sms_alert(self, message):
        """Trigger SMS alert (placeholder)."""
        # In production, integrate with SMS API (Twilio, etc.)
        print(f"SMS Alert to {self.preferences.phone_number}: {message}")
    
    def _trigger_email_alert(self, message):
        """Trigger email alert (placeholder)."""
        # In production, integrate with email service
        print(f"Email Alert to {self.preferences.email}: {message}")
    
    def get_recent_alerts(self, limit=10):
        """Get recent alerts for the session."""
        return AlertHistory.objects.filter(
            session=self.session
        ).order_by('-timestamp')[:limit]
    
    def acknowledge_alert(self, alert_id):
        """Acknowledge an alert."""
        try:
            alert = AlertHistory.objects.get(id=alert_id, user=self.user)
            alert.acknowledged = True
            alert.save()
            return True
        except AlertHistory.DoesNotExist:
            return False
    
    def get_alert_statistics(self):
        """Get alert statistics for the session."""
        alerts = AlertHistory.objects.filter(session=self.session)
        
        return {
            'total_alerts': alerts.count(),
            'audio_alerts': alerts.filter(alert_type='AUDIO').count(),
            'visual_alerts': alerts.filter(alert_type='VISUAL').count(),
            'sms_alerts': alerts.filter(alert_type='SMS').count(),
            'email_alerts': alerts.filter(alert_type='EMAIL').count(),
            'high_severity': alerts.filter(severity='HIGH').count(),
            'medium_severity': alerts.filter(severity='MEDIUM').count(),
            'low_severity': alerts.filter(severity='LOW').count(),
            'acknowledged': alerts.filter(acknowledged=True).count(),
            'unacknowledged': alerts.filter(acknowledged=False).count(),
        }
