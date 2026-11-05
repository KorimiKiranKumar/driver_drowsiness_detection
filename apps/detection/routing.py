"""
WebSocket Routing Configuration
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/detection/(?P<session_id>\d+)/$', consumers.DetectionConsumer.as_asgi()),
]
