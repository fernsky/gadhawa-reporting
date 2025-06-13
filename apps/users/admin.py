"""
Django admin configuration for Users app
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone

from .models import User, UserSession


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin with additional fields and security features
    """
    
    list_display = [
        'username', 
        'full_name_nepali', 
        'email', 
        'role', 
        'is_verified',
        'is_active', 
        'ward_number',
        'failed_login_attempts',
        'created_at'
    ]
    
    list_filter = [
        'role', 
        'is_active', 
        'is_verified', 
        'ward_number',
        'created_at',
        'last_login'
    ]
    
    search_fields = [
        'username', 
        'email', 
        'full_name_nepali', 
        'first_name', 
        'last_name',
        'phone_number'
    ]
    
    readonly_fields = [
        'id',
        'created_at', 
        'updated_at', 
        'last_password_change',
        'failed_login_attempts',
        'account_locked_until',
        'session_info'
    ]
    
    ordering = ['-created_at']
    
    # Fieldsets for organizing the admin form
    fieldsets = (
        (_('खाता जानकारी'), {  # Account Information
            'fields': (
                'id',
                'username', 
                'password',
                'email',
                'role',
                'is_verified'
            )
        }),
        (_('व्यक्तिगत जानकारी'), {  # Personal Information
            'fields': (
                'first_name', 
                'last_name',
                'full_name_nepali',
                'phone_number',
                'profile_picture'
            )
        }),
        (_('कार्यक्षेत्र'), {  # Work Area
            'fields': (
                'position',
                'position_nepali',
                'department',
                'ward_number'
            )
        }),
        (_('अनुमतिहरू'), {  # Permissions
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser',
                'groups', 
                'user_permissions'
            ),
            'classes': ('collapse',)
        }),
        (_('सुरक्षा जानकारी'), {  # Security Information
            'fields': (
                'last_password_change',
                'failed_login_attempts',
                'account_locked_until',
                'last_login',
                'session_info'
            ),
            'classes': ('collapse',)
        }),
        (_('समयस्टाम्प'), {  # Timestamps
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    # Fieldsets for adding new user
    add_fieldsets = (
        (_('आधारभूत जानकारी'), {  # Basic Information
            'classes': ('wide',),
            'fields': (
                'username', 
                'email',
                'password1', 
                'password2',
                'role'
            ),
        }),
        (_('व्यक्तिगत जानकारी'), {  # Personal Information
            'classes': ('wide',),
            'fields': (
                'first_name',
                'last_name', 
                'full_name_nepali',
                'phone_number'
            ),
        }),
        (_('कार्यक्षेत्र'), {  # Work Area
            'classes': ('wide',),
            'fields': (
                'position',
                'position_nepali',
                'department',
                'ward_number'
            ),
        }),
    )
    
    def session_info(self, obj):
        """Display active sessions info"""
        active_sessions = obj.sessions.filter(is_active=True).count()
        if active_sessions > 0:
            return format_html(
                '<span style="color: green;">सक्रिय सेसनहरू: {}</span>',
                active_sessions
            )
        return 'कुनै सक्रिय सेसन छैन'
    
    session_info.short_description = _('सेसन जानकारी')  # Session Information
    
    def get_queryset(self, request):
        """Optimize queryset with prefetch_related"""
        return super().get_queryset(request).prefetch_related('sessions')
    
    def save_model(self, request, obj, form, change):
        """Custom save to handle password changes"""
        if change and 'password' in form.changed_data:
            obj.last_password_change = timezone.now()
        super().save_model(request, obj, form, change)
    
    actions = ['verify_users', 'reset_failed_attempts', 'deactivate_users']
    
    def verify_users(self, request, queryset):
        """Verify selected users"""
        updated = queryset.update(is_verified=True)
        self.message_user(
            request,
            f'{updated} प्रयोगकर्ता प्रमाणित गरियो।'
        )
    verify_users.short_description = _('चयनित प्रयोगकर्ताहरूलाई प्रमाणित गर्नुहोस्')
    
    def reset_failed_attempts(self, request, queryset):
        """Reset failed login attempts for selected users"""
        for user in queryset:
            user.reset_failed_login_attempts()
        self.message_user(
            request,
            f'{queryset.count()} प्रयोगकर्ताका असफल प्रयासहरू रिसेट गरियो।'
        )
    reset_failed_attempts.short_description = _('असफल लगइन प्रयासहरू रिसेट गर्नुहोस्')
    
    def deactivate_users(self, request, queryset):
        """Deactivate selected users"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} प्रयोगकर्ता निष्क्रिय गरियो।'
        )
    deactivate_users.short_description = _('चयनित प्रयोगकर्ताहरूलाई निष्क्रिय गर्नुहोस्')


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """
    Admin for User Sessions - for security monitoring
    """
    
    list_display = [
        'user',
        'ip_address',
        'login_time',
        'logout_time',
        'is_active',
        'session_duration'
    ]
    
    list_filter = [
        'is_active',
        'login_time',
        'logout_time',
        'user__role'
    ]
    
    search_fields = [
        'user__username',
        'user__email',
        'ip_address',
        'session_key'
    ]
    
    readonly_fields = [
        'id',
        'session_key',
        'login_time',
        'session_duration'
    ]
    
    ordering = ['-login_time']
    
    def session_duration(self, obj):
        """Calculate session duration"""
        if obj.logout_time:
            duration = obj.logout_time - obj.login_time
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
        elif obj.is_active:
            duration = timezone.now() - obj.login_time
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours)}h {int(minutes)}m {int(seconds)}s (सक्रिय)"
        return "N/A"
    
    session_duration.short_description = _('सेसन अवधि')  # Session Duration
    
    def has_add_permission(self, request):
        """Disable adding sessions manually"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Allow only logout_time changes"""
        return True
    
    def get_readonly_fields(self, request, obj=None):
        """Make most fields readonly"""
        if obj:  # Editing existing object
            return self.readonly_fields + ['user', 'ip_address', 'user_agent']
        return self.readonly_fields
    
    actions = ['end_sessions']
    
    def end_sessions(self, request, queryset):
        """End selected active sessions"""
        active_sessions = queryset.filter(is_active=True)
        for session in active_sessions:
            session.logout_time = timezone.now()
            session.is_active = False
            session.save()
        
        self.message_user(
            request,
            f'{active_sessions.count()} सेसनहरू समाप्त गरियो।'
        )
    end_sessions.short_description = _('चयनित सेसनहरू समाप्त गर्नुहोस्')
