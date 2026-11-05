from django.urls import path
from . import views

app_name = 'alerts'

urlpatterns = [
    path('', views.preferences_page, name='alerts'),
    path('log/', views.alerts_page, name='alert_log'),
    path('acknowledge/<int:alert_id>/', views.acknowledge_alert, name='acknowledge_alert'),
    path('detail/<int:alert_id>/', views.alert_detail, name='alert_detail'),
]