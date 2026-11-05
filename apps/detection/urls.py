from django.urls import path
from . import views

app_name = 'detection'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('monitor/', views.monitor, name='monitor'),
    path('detect/', views.detect, name='detect'),
    path('stop/', views.stop_session, name='stop_session'),
    path('results/', views.results, name='results'),
]