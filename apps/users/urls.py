"""
URL configuration for Users app.
"""

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token-refresh'),
    
    # Profile management
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('change-password/', views.PasswordChangeView.as_view(), name='change-password'),
    
    # User management (Admin/Manager only)
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<uuid:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    
    # Session management
    path('sessions/', views.UserSessionListView.as_view(), name='session-list'),
    path('sessions/end/', views.end_session, name='end-session'),
]
