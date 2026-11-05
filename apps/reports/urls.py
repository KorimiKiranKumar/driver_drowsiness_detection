from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports, name='reports'),
    path('charts/', views.charts, name='charts'),
    path('session/<int:session_id>/', views.session_report, name='session_report'),
]