import os
from django.core.asgi import get_asgi_application

# Set the Django settings module first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'driver_drowsiness_system.settings')

# Initialize Django ASGI application early to ensure AppRegistry
# and settings are fully loaded before importing models or routing
django_asgi_app = get_asgi_application()

# Import Channels routing after Django is initialized
from channels.routing import ProtocolTypeRouter, URLRouter
from apps.detection.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(websocket_urlpatterns),
})
