from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone

from .models import AlertHistory, AlertPreference
from django.contrib import messages


def alerts_page(request):
    if not request.user.is_authenticated:
        return render(request, 'alerts/alert_log.html', {
            'alerts': [],
            'total_alerts': 0,
            'critical_alerts': 0,
            'acknowledged_alerts': 0,
            'today_alerts': 0,
        })

    alerts_query = AlertHistory.objects.filter(user=request.user).order_by('-timestamp')

    severity = request.GET.get('severity')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if severity:
        alerts_query = alerts_query.filter(severity=severity.upper())
    if date_from:
        alerts_query = alerts_query.filter(timestamp__date__gte=date_from)
    if date_to:
        alerts_query = alerts_query.filter(timestamp__date__lte=date_to)

    if settings.USE_TZ:
        today = timezone.localdate()
    else:
        today = timezone.now().date()

    today_alerts = AlertHistory.objects.filter(user=request.user, timestamp__date=today).count()

    return render(request, 'alerts/alert_log.html', {
        'alerts': alerts_query,
        'total_alerts': alerts_query.count(),
        'critical_alerts': alerts_query.filter(severity='CRITICAL').count(),
        'acknowledged_alerts': alerts_query.filter(acknowledged=True).count(),
        'today_alerts': today_alerts,
    })


def acknowledge_alert(request, alert_id):
    if request.method != 'POST' or not request.user.is_authenticated:
        return JsonResponse({'success': False}, status=400)

    alert = get_object_or_404(AlertHistory, id=alert_id, user=request.user)
    alert.acknowledged = True
    alert.save()

    return JsonResponse({'success': True})


def alert_detail(request, alert_id):
    alert = get_object_or_404(AlertHistory, id=alert_id, user=request.user)

    return JsonResponse({
        'id': alert.id,
        'timestamp': alert.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'severity': alert.severity,
        'severity_color': 'danger' if alert.severity == 'CRITICAL' else ('warning' if alert.severity == 'HIGH' else 'info'),
        'alert_type': alert.alert_type,
        'message': alert.message,
        'session_id': alert.session.id if alert.session else None,
        'acknowledged': alert.acknowledged,
    })

def preferences_page(request):
    if not request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('accounts:login')
        
    preference, created = AlertPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        preference.audio_enabled = 'sound_enabled' in request.POST
        preference.visual_enabled = 'visual_enabled' in request.POST
        preference.sound_volume = int(request.POST.get('sound_volume', 80))
        preference.sound_type = request.POST.get('sound_type', 'beep')
        preference.visual_intensity = request.POST.get('visual_intensity', 'medium')
        preference.visual_color = request.POST.get('visual_color', 'red')
        preference.drowsiness_threshold = int(request.POST.get('drowsiness_threshold', 70))
        preference.alert_delay = int(request.POST.get('alert_delay', 3))
        
        preference.save()
        messages.success(request, 'Alert preferences updated successfully.')
        from django.shortcuts import redirect
        return redirect('alerts:alerts')
        
    preferences_context = {
        'sound_enabled': preference.audio_enabled,
        'visual_enabled': preference.visual_enabled,
        'sound_volume': preference.sound_volume,
        'sound_type': preference.sound_type,
        'visual_intensity': preference.visual_intensity,
        'visual_color': preference.visual_color,
        'drowsiness_threshold': preference.drowsiness_threshold,
        'alert_delay': preference.alert_delay,
    }
    
    return render(request, 'alerts/preferences.html', {'preferences': preferences_context})