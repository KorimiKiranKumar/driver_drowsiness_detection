from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache

import base64
import json
import cv2
import numpy as np
import logging

from .models import DriverSession, DrowsinessEvent
from .utils.feature_extractor import FeatureExtractor
import mediapipe as mp

logger = logging.getLogger(__name__)

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    # Iris landmarks are not needed for EAR/MAR and add substantial work per frame.
    refine_landmarks=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
feature_extractor = FeatureExtractor()

RUNTIME_TTL = 60 * 60


def runtime_key(session_id):
    return f'detection-runtime:{session_id}'


def new_runtime(session):
    return {
        'closed_frames': 0,
        'eye_was_closed': False,
        'blink_count': session.blink_count,
        'drowsy_count': session.drowsy_count,
        'alert_count': session.total_alerts_triggered,
        'total_frames': session.total_frames,
        'pose_history': {
            'STRAIGHT': session.head_straight_count,
            'UP': session.head_up_count,
            'DOWN': session.head_down_count,
            'LEFT': session.head_left_count,
            'RIGHT': session.head_right_count,
        },
    }


def dashboard(request):
    if request.user.is_authenticated:
        sessions = DriverSession.objects.filter(user=request.user)
    else:
        sessions = DriverSession.objects.filter(user=None)
    total_sessions = sessions.count()
    total_drowsiness_events = DrowsinessEvent.objects.filter(session__in=sessions).count()
    total_alerts = sessions.aggregate(total_alerts=Sum('total_alerts_triggered'))['total_alerts'] or 0
    safety_score = max(0, 100 - min(100, total_alerts * 2))
    return render(request, 'detection/dashboard.html', {
        'total_sessions': total_sessions,
        'total_events': total_drowsiness_events,
        'total_alerts': total_alerts,
        'safety_score': safety_score,
    })

def monitor(request):
    request.session.pop('session_id', None)
    return render(request, 'detection/monitor.html')

def stop_session(request):
    session_id = request.session.get('session_id')
    if session_id:
        runtime = cache.get(runtime_key(session_id))
        update_values = {'end_time': timezone.now()}
        if runtime:
            update_values.update({
                'blink_count': runtime['blink_count'],
                'drowsy_count': runtime['drowsy_count'],
                'total_alerts_triggered': runtime['alert_count'],
                'total_frames': runtime['total_frames'],
                'head_straight_count': runtime['pose_history']['STRAIGHT'],
                'head_up_count': runtime['pose_history']['UP'],
                'head_down_count': runtime['pose_history']['DOWN'],
                'head_left_count': runtime['pose_history']['LEFT'],
                'head_right_count': runtime['pose_history']['RIGHT'],
            })
        DriverSession.objects.filter(id=session_id, end_time__isnull=True).update(**update_values)
        cache.delete(runtime_key(session_id))
    request.session.pop('session_id', None)
    return JsonResponse({'status': 'stopped'})

def results(request):
    session_id = request.session.get("session_id")
    if request.user.is_authenticated:
        sessions = DriverSession.objects.filter(user=request.user).order_by('-start_time')
    else:
        sessions = DriverSession.objects.filter(user=None).order_by('-start_time')
    active_session = sessions.filter(id=session_id).first() if session_id else sessions.first()
    return render(request, 'detection/results.html', {
        'session': active_session,
        'sessions': sessions,
        'blink_count': active_session.blink_count if active_session else 0,
        'drowsy_count': active_session.drowsy_count if active_session else 0,
    })

def detect(request):
    if request.method != "POST":
        return JsonResponse({"status": "Invalid Request", "error": True})
    try:
        image_data = request.POST.get("image")
        if not image_data and request.content_type.startswith('application/json'):
            payload = json.loads(request.body.decode('utf-8') or '{}')
            image_data = payload.get('image')
        if not image_data:
            return JsonResponse({"status": "No Image", "error": True})
        
        if len(image_data) > 2_000_000:
            return JsonResponse({"status": "Frame Too Large", "error": True}, status=413)
        _, imgstr = image_data.split(';base64,', 1)
        img_bytes = base64.b64decode(imgstr)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if frame is None: return JsonResponse({"status": "Invalid Frame", "error": True})

        # The browser captures at 640x480. Do not upscale each received frame.
        if frame.shape[1] > 640:
            scale = 640 / frame.shape[1]
            frame = cv2.resize(frame, (640, int(frame.shape[0] * scale)))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        session_id = request.session.get("session_id")
        runtime = cache.get(runtime_key(session_id)) if session_id else None
        if not session_id or runtime is None:
            session = DriverSession.objects.filter(id=session_id, end_time__isnull=True).first() if session_id else None
        else:
            session = None
        if not session_id or (runtime is None and not session):
            session = DriverSession.objects.create(user=request.user if request.user.is_authenticated else None)
            request.session["session_id"] = session.id
            session_id = session.id
        if runtime is None:
            runtime = new_runtime(session)

        results = face_mesh.process(rgb_frame)
        
        state, head_pose, is_drowsy = "Awake 😃", "STRAIGHT", False
        avg_ear, mar_value = 0.0, 0.0
        landmarks_data = {}
        face_detected = False

        if results.multi_face_landmarks:
            face_detected = True
            landmarks = results.multi_face_landmarks[0].landmark
            h, w = frame.shape[:2]
            # Convert normalized landmarks to pixel coordinates
            pts = [(int(l.x * w), int(l.y * h)) for l in landmarks]
            # Send only points used by the overlay, not all 468 landmarks.
            overlay_indices = set(feature_extractor.LEFT_EYE + feature_extractor.RIGHT_EYE + [13, 14, 78, 308])
            landmarks_data = {str(i): pts[i] for i in overlay_indices}
            
            # Calculate EAR and MAR
            left_ear = feature_extractor.calculate_ear(pts, feature_extractor.LEFT_EYE)
            right_ear = feature_extractor.calculate_ear(pts, feature_extractor.RIGHT_EYE)
            avg_ear = (left_ear + right_ear) / 2.0
            mar_value = feature_extractor.calculate_mar(pts)
            
            # Head Pose Estimation
            head_pose = feature_extractor.estimate_head_pose(pts, frame.shape)

        # State Machine (User Requirements: EAR_T=0.23, BLINK_F=2, DROWSY_F=15)
        EAR_THRESHOLD = 0.23
        BLINK_FRAMES = 2
        DROWSY_FRAMES = 15
        
        closed_f = runtime['closed_frames']
        was_closed = runtime['eye_was_closed']
        is_closed = avg_ear < EAR_THRESHOLD if face_detected else False

        if not face_detected:
            state, closed_f = "No Face ❌", 0
        elif not is_closed:
            if was_closed and BLINK_FRAMES <= closed_f < DROWSY_FRAMES:
                runtime['blink_count'] += 1
                DrowsinessEvent.objects.create(session_id=session_id, severity='LOW', ear=avg_ear, mar=mar_value, head_pose=head_pose)
            state, closed_f, was_closed = "Awake 😃", 0, False
        else:
            closed_f += 1
            was_closed = True
            if closed_f < BLINK_FRAMES:
                state = "Blinking 👁️"
            elif closed_f < DROWSY_FRAMES:
                state = "Blinking 👁️"
            else:
                state, is_drowsy = "Drowsy 😴", True
                if closed_f == DROWSY_FRAMES:
                    runtime['drowsy_count'] += 1
                    runtime['alert_count'] += 1
                    DrowsinessEvent.objects.create(session_id=session_id, severity='HIGH', ear=avg_ear, mar=mar_value, head_pose=head_pose)

        # Keep high-frequency counters in the cache and persist once on stop.
        runtime['total_frames'] += 1
        pose_map = {"STRAIGHT": 'head_straight_count', "UP": 'head_up_count', "DOWN": 'head_down_count', "LEFT": 'head_left_count', "RIGHT": 'head_right_count'}
        if head_pose in pose_map:
            runtime['pose_history'][head_pose] += 1
        runtime['closed_frames'] = closed_f
        runtime['eye_was_closed'] = was_closed
        cache.set(runtime_key(session_id), runtime, RUNTIME_TTL)

        return JsonResponse({
            "session_id": session_id,
            "status": state, 
            "is_drowsy": is_drowsy, 
            "ear": round(avg_ear, 3), 
            "mar": round(mar_value, 3),
            "head_pose": head_pose, 
            "blink_count": runtime['blink_count'],
            "drowsy_count": runtime['drowsy_count'],
            "alert_count": runtime['alert_count'],
            "pose_history": runtime['pose_history'],
            "landmarks": landmarks_data, 
            "error": False
        })
    except Exception:
        logger.exception('Detection request failed')
        return JsonResponse({"status": "System Error", "error": True}, status=500)
