from django.urls import path, include
from django.shortcuts import redirect
from django.http import JsonResponse

def redirect_to_login(request):
    return redirect('accounts:login')


def health(request):
    """Lightweight endpoint used by the deployment platform."""
    return JsonResponse({'status': 'ok'})

urlpatterns = [
    path('health/', health, name='health'),
    path('', redirect_to_login, name='home'),
    path('detection/', include('apps.detection.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('reports/', include('apps.reports.urls')),   # ✅ IMPORTANT
]
