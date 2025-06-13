"""
Serializers for Users app - API data serialization
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import User, UserSession


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model - public information only
    """
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name_nepali',
            'role',
            'position',
            'position_nepali',
            'department',
            'ward_number',
            'is_verified',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for User profile - detailed information for the user themselves
    """
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name_nepali',
            'phone_number',
            'role',
            'position',
            'position_nepali',
            'department',
            'ward_number',
            'profile_picture',
            'is_verified',
            'last_login',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id', 
            'username', 
            'role', 
            'ward_number', 
            'is_verified',
            'last_login',
            'created_at', 
            'updated_at'
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new users
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'full_name_nepali',
            'phone_number',
            'role',
            'position',
            'position_nepali',
            'department',
            'ward_number'
        ]
    
    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                _('पासवर्ड मिलेन।')  # Passwords don't match
            )
        return attrs
    
    def validate_ward_number(self, value):
        """Validate ward number"""
        if value is not None and (value < 1 or value > 8):
            raise serializers.ValidationError(
                _('वडा नम्बर १ देखि ८ सम्म हुनुपर्छ।')  # Ward number must be 1-8
            )
        return value
    
    def create(self, validated_data):
        """Create user with encrypted password"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.last_password_change = timezone.now()
        user.save()
        
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer with additional security
    """
    
    def validate(self, attrs):
        """Custom validation with security checks"""
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            try:
                user = User.objects.get(username=username)
                
                # Check if account is locked
                if user.is_account_locked():
                    raise serializers.ValidationError(
                        _('खाता अस्थायी रूपमा लक गरिएको छ। कृपया पछि प्रयास गर्नुहोस्।')
                        # Account is temporarily locked. Please try again later.
                    )
                
                # Check if account is active
                if not user.is_active:
                    raise serializers.ValidationError(
                        _('यो खाता निष्क्रिय छ।')  # This account is inactive
                    )
                
            except User.DoesNotExist:
                pass  # Let Django handle the authentication
        
        # Attempt authentication
        try:
            data = super().validate(attrs)
            
            # Reset failed attempts on successful login
            user = self.user
            if user.failed_login_attempts > 0:
                user.reset_failed_login_attempts()
            
            return data
            
        except Exception as e:
            # Increment failed login attempts
            if username:
                try:
                    user = User.objects.get(username=username)
                    user.increment_failed_login_attempts()
                except User.DoesNotExist:
                    pass
            
            raise e
    
    @classmethod
    def get_token(cls, user):
        """Add custom claims to token"""
        token = super().get_token(user)
        
        # Add custom claims
        token['role'] = user.role
        token['ward_number'] = user.ward_number
        token['full_name'] = user.get_full_name()
        token['is_verified'] = user.is_verified
        
        return token


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing password
    """
    old_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate_old_password(self, value):
        """Validate old password"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('पुरानो पासवर्ड गलत छ।')  # Old password is incorrect
            )
        return value
    
    def validate(self, attrs):
        """Validate new password confirmation"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                _('नयाँ पासवर्ड मिलेन।')  # New passwords don't match
            )
        return attrs
    
    def save(self):
        """Change user password"""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.last_password_change = timezone.now()
        user.save()
        return user


class UserSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for User Sessions
    """
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = UserSession
        fields = [
            'id',
            'session_key',
            'ip_address',
            'user_agent',
            'login_time',
            'logout_time',
            'is_active',
            'duration'
        ]
        read_only_fields = ['id', 'session_key', 'login_time']
    
    def get_duration(self, obj):
        """Calculate session duration"""
        if obj.logout_time:
            duration = obj.logout_time - obj.login_time
        elif obj.is_active:
            duration = timezone.now() - obj.login_time
        else:
            return None
        
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return {
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'total_seconds': total_seconds
        }
