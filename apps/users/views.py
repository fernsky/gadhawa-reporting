"""
API Views for Users app - Authentication and user management
"""

from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import User, UserSession
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserCreateSerializer,
    CustomTokenObtainPairSerializer,
    PasswordChangeSerializer,
    UserSessionSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT login view with session tracking
    """
    serializer_class = CustomTokenObtainPairSerializer
    
    @extend_schema(
        summary="प्रयोगकर्ता लगइन",  # User Login
        description="प्रयोगकर्तानाम र पासवर्ड प्रयोग गरेर JWT टोकन प्राप्त गर्नुहोस्",
        responses={200: CustomTokenObtainPairSerializer}
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Create session record for successful login
            user = User.objects.get(username=request.data.get('username'))
            
            # Get client information
            ip_address = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # Create session record
            UserSession.objects.create(
                user=user,
                session_key=request.session.session_key or 'api_session',
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            # Add user info to response
            response.data['user'] = UserSerializer(user).data
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LogoutView(APIView):
    """
    Logout view - blacklist refresh token and end session
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="प्रयोगकर्ता लगआउट",  # User Logout
        description="हालको सेसन समाप्त गर्नुहोस् र टोकन ब्ल्याकलिस्ट गर्नुहोस्",
        responses={200: {"type": "object", "properties": {"message": {"type": "string"}}}}
    )
    def post(self, request):
        try:
            # Get refresh token from request
            refresh_token = request.data.get("refresh_token")
            
            if refresh_token:
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            # End user session
            UserSession.objects.filter(
                user=request.user,
                is_active=True
            ).update(
                logout_time=timezone.now(),
                is_active=False
            )
            
            return Response(
                {"message": _("सफलतापूर्वक लगआउट भयो।")},  # Successfully logged out
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {"error": _("लगआउट गर्दा त्रुटि भयो।")},  # Error during logout
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and update user profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    @extend_schema(
        summary="प्रयोगकर्ता प्रोफाइल हेर्नुहोस्",  # View User Profile
        description="हालको प्रयोगकर्ताको प्रोफाइल जानकारी प्राप्त गर्नुहोस्",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="प्रयोगकर्ता प्रोफाइल अपडेट गर्नुहोस्",  # Update User Profile
        description="प्रयोगकर्ताको प्रोफाइल जानकारी अपडेट गर्नुहोस्",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class PasswordChangeView(APIView):
    """
    Change user password
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="पासवर्ड परिवर्तन गर्नुहोस्",  # Change Password
        description="प्रयोगकर्ताको पासवर्ड परिवर्तन गर्नुहोस्",
        request=PasswordChangeSerializer,
        responses={200: {"type": "object", "properties": {"message": {"type": "string"}}}}
    )
    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": _("पासवर्ड सफलतापूर्वक परिवर्तन भयो।")},  # Password changed successfully
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserListCreateView(generics.ListCreateAPIView):
    """
    List users and create new users (Admin only)
    """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
    
    def get_queryset(self):
        """Filter users based on permissions"""
        user = self.request.user
        
        if user.is_admin():
            return User.objects.all()
        elif user.is_manager():
            return User.objects.filter(role__in=[
                User.UserRole.DATA_ENTRY,
                User.UserRole.VIEWER,
                User.UserRole.WARD_OFFICER
            ])
        else:
            return User.objects.filter(id=user.id)
    
    def perform_create(self, serializer):
        """Only admins can create users"""
        if not self.request.user.is_admin():
            raise permissions.PermissionDenied(
                _("प्रयोगकर्ता सिर्जना गर्ने अनुमति छैन।")  # No permission to create users
            )
        serializer.save()
    
    @extend_schema(
        summary="प्रयोगकर्ता सूची",  # User List
        description="सबै प्रयोगकर्ताहरूको सूची प्राप्त गर्नुहोस्",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="नयाँ प्रयोगकर्ता सिर्जना गर्नुहोस्",  # Create New User
        description="नयाँ प्रयोगकर्ता खाता सिर्जना गर्नुहोस् (प्रशासकका लागि मात्र)",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update, or delete specific user (Admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter users based on permissions"""
        user = self.request.user
        
        if user.is_admin():
            return User.objects.all()
        elif user.is_manager():
            return User.objects.filter(role__in=[
                User.UserRole.DATA_ENTRY,
                User.UserRole.VIEWER,
                User.UserRole.WARD_OFFICER
            ])
        else:
            return User.objects.filter(id=user.id)
    
    def perform_update(self, serializer):
        """Check permissions for user updates"""
        user = self.request.user
        target_user = self.get_object()
        
        # Users can only update their own profile (limited fields)
        if user.id == target_user.id:
            # Allow self-update
            pass
        elif user.is_admin():
            # Admins can update anyone
            pass
        elif user.is_manager() and target_user.role in [
            User.UserRole.DATA_ENTRY,
            User.UserRole.VIEWER,
            User.UserRole.WARD_OFFICER
        ]:
            # Managers can update lower-level users
            pass
        else:
            raise permissions.PermissionDenied(
                _("यो प्रयोगकर्ता अपडेट गर्ने अनुमति छैन।")  # No permission to update this user
            )
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Only admins can delete users"""
        if not self.request.user.is_admin():
            raise permissions.PermissionDenied(
                _("प्रयोगकर्ता मेटाउने अनुमति छैन।")  # No permission to delete users
            )
        instance.delete()


class UserSessionListView(generics.ListAPIView):
    """
    List user sessions for security monitoring
    """
    serializer_class = UserSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return sessions for current user or all sessions for admins"""
        user = self.request.user
        
        if user.is_admin():
            return UserSession.objects.all()
        else:
            return UserSession.objects.filter(user=user)
    
    @extend_schema(
        summary="प्रयोगकर्ता सेसन सूची",  # User Session List
        description="प्रयोगकर्ता सेसनहरूको सूची (सुरक्षा निगरानीका लागि)",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@extend_schema(
    summary="सेसन समाप्त गर्नुहोस्",  # End Session
    description="निर्दिष्ट सेसन समाप्त गर्नुहोस्",
    request={"type": "object", "properties": {"session_id": {"type": "string"}}},
    responses={200: {"type": "object", "properties": {"message": {"type": "string"}}}}
)
def end_session(request):
    """
    End a specific session
    """
    session_id = request.data.get('session_id')
    
    if not session_id:
        return Response(
            {"error": _("सेसन ID आवश्यक छ।")},  # Session ID required
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Get session
        if request.user.is_admin():
            session = UserSession.objects.get(id=session_id)
        else:
            session = UserSession.objects.get(id=session_id, user=request.user)
        
        # End session
        session.logout_time = timezone.now()
        session.is_active = False
        session.save()
        
        return Response(
            {"message": _("सेसन सफलतापूर्वक समाप्त भयो।")},  # Session ended successfully
            status=status.HTTP_200_OK
        )
        
    except UserSession.DoesNotExist:
        return Response(
            {"error": _("सेसन फेला परेन।")},  # Session not found
            status=status.HTTP_404_NOT_FOUND
        )
