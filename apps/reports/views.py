import json
from datetime import date, timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, Min, Max
from django.db.models.functions import TruncDate
from apps.detection.models import DriverSession, DrowsinessEvent
from apps.alerts.models import AlertHistory


@login_required
def reports(request):
    sessions = DriverSession.objects.filter(user=request.user).order_by('-start_time')
    total_sessions = sessions.count()
    completed_sessions = sessions.filter(end_time__isnull=False).count()
    total_duration = sum((s.duration for s in sessions))

    aggregate_data = sessions.aggregate(
        total_blinks=Sum('blink_count'),
        total_drowsy=Sum('drowsy_count')
    )

    total_blinks = aggregate_data.get('total_blinks') or 0
    total_drowsy = aggregate_data.get('total_drowsy') or 0

    return render(request, 'reports/reports.html', {
        'sessions': sessions,
        'total_sessions': total_sessions,
        'completed_sessions': completed_sessions,
        'total_duration': total_duration,
        'total_blinks': total_blinks,
        'total_drowsy': total_drowsy,
    })


@login_required
def charts(request):
    sessions = DriverSession.objects.filter(user=request.user)
    events = DrowsinessEvent.objects.filter(session__in=sessions)
    alerts_qs = AlertHistory.objects.filter(user=request.user)

    today = date.today()
    start_date = today - timedelta(days=6)

    drowsy_by_day = (
        events
        .filter(timestamp__date__range=[start_date, today])
        .annotate(day=TruncDate('timestamp'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    alert_by_day = (
        alerts_qs
        .filter(timestamp__date__range=[start_date, today])
        .annotate(day=TruncDate('timestamp'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    date_counts = {x['day'].strftime('%b %d'): x['count'] for x in drowsy_by_day}
    alert_counts = {x['day'].strftime('%b %d'): x['count'] for x in alert_by_day}

    full_dates = []
    full_drowsy = []
    full_alerts = []
    for i in range(7):
        d = start_date + timedelta(days=i)
        label = d.strftime('%b %d')
        full_dates.append(label)
        full_drowsy.append(date_counts.get(label, 0))
        full_alerts.append(alert_counts.get(label, 0))

    total_blinks = sessions.aggregate(total=Sum('blink_count')).get('total') or 0
    total_drowsy = sessions.aggregate(total=Sum('drowsy_count')).get('total') or 0

    avg_ear = events.aggregate(avg=Avg('ear')).get('avg') or 0
    avg_mar = events.aggregate(avg=Avg('mar')).get('avg') or 0

    durations_minutes = [round((s.duration / 60.0), 2) for s in sessions.order_by('-start_time')[:7]]

    return render(request, 'reports/charts.html', {
        'total_sessions': sessions.count(),
        'total_drowsy_events': total_drowsy,
        'total_blinks': total_blinks,
        'total_alerts': alerts_qs.count(),
        'avg_ear': avg_ear,
        'avg_mar': avg_mar,
        'dates': json.dumps(full_dates),
        'drowsy_events': json.dumps(full_drowsy),
        'alerts': json.dumps(full_alerts),
        'durations': json.dumps(durations_minutes),
    })

@login_required
def session_report(request, session_id):
    session = DriverSession.objects.filter(id=session_id, user=request.user).first()
    if not session:
        return render(request, 'reports/session_report.html', {
            'error': 'Session not found.'
        })

    events = DrowsinessEvent.objects.filter(session=session)

    # severity breakdown
    normal_count = events.filter(severity__in=['LOW', 'NORMAL']).count()
    medium_count = events.filter(severity__in=['MEDIUM']).count()
    high_count = events.filter(severity__in=['HIGH', 'CRITICAL']).count()

    # head pose distribution (Using direct session counters for accuracy)
    head_straight = session.head_straight_count
    head_up = session.head_up_count
    head_left = session.head_left_count
    head_right = session.head_right_count
    head_down = session.head_down_count

    avg_ear = events.aggregate(avg=Avg('ear')).get('avg') or 0
    min_ear = events.aggregate(min=Min('ear')).get('min') or 0
    max_ear = events.aggregate(max=Max('ear')).get('max') or 0

    avg_mar = events.aggregate(avg=Avg('mar')).get('avg') or 0
    min_mar = events.aggregate(min=Min('mar')).get('min') or 0
    max_mar = events.aggregate(max=Max('mar')).get('max') or 0

    report_data = {
        'total_duration_seconds': session.duration,
        'total_frames_processed': session.total_frames_processed,
        'total_blinks': session.blink_count,
        'total_drowsy_events': session.drowsy_count,
        'total_alerts_triggered': session.total_alerts_triggered,
        'average_ear': avg_ear,
        'min_ear': min_ear,
        'max_ear': max_ear,
        'average_mar': avg_mar,
        'min_mar': min_mar,
        'max_mar': max_mar,
        'normal_frames': normal_count,
        'medium_drowsy_frames': medium_count,
        'high_drowsy_frames': high_count,
        'head_straight_count': head_straight,
        'head_up_count': head_up,
        'head_left_count': head_left,
        'head_right_count': head_right,
        'head_down_count': head_down,
    }

    return render(request, 'reports/session_report.html', {
        'session': session,
        'events': events,
        'drowsiness_events': events,
        'report': report_data,
        'session_label': f"Session #{session.id}",
    })
