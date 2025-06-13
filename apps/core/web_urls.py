"""
Web URLs for core app (template-based views).
"""

from django.urls import path
from . import web_views

app_name = 'core_web'

urlpatterns = [
    # Main dashboard
    path('', web_views.DashboardView.as_view(), name='dashboard'),
    
    # Authentication pages
    path('login/', web_views.LoginView.as_view(), name='login'),
    path('logout/', web_views.LogoutView.as_view(), name='logout'),
    
    # Profile pages
    path('profile/', web_views.ProfileView.as_view(), name='profile'),
]
