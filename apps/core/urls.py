"""
Core API URLs for Gadhawa Report System.
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Health check and system info
    path('health/', views.HealthCheckView.as_view(), name='health-check'),
    path('system-info/', views.SystemInfoView.as_view(), name='system-info'),
    
    # Municipality information
    path('municipality-info/', views.MunicipalityInfoView.as_view(), name='municipality-info'),
]
