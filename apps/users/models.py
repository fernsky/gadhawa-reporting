"""
Custom User model for gadhawa Report System

This model extends Django's AbstractUser to add custom fields
specific to the GadhawaMunicipality reporting system.
"""

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model with additional fields for GadhawaReport System
    """

    # Use UUID as primary key for better security
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # User roles specific to municipality operations
    class UserRole(models.TextChoices):
        ADMIN = "admin", _("प्रशासक")  # Administrator
        MANAGER = "manager", _("प्रबन्धक")  # Manager
        DATA_ENTRY = "data_entry", _("डाटा एन्ट्री")  # Data Entry
        VIEWER = "viewer", _("दर्शक")  # Viewer
        WARD_OFFICER = "ward_officer", _("वडा अधिकारी")  # Ward Officer

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.VIEWER,
        verbose_name=_("भूमिका"),  # Role
    )

    # Additional user information
    full_name_nepali = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("पूरा नाम (नेपालीमा)"),  # Full Name in Nepali
    )

    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name=_("फोन नम्बर")  # Phone Number
    )

    position = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("पद")  # Position
    )

    position_nepali = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("पद (नेपालीमा)"),  # Position in Nepali
    )

    department = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("विभाग")  # Department
    )

    ward_number = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("वडा नं"),  # Ward Number
        help_text=_("वडा अधिकारीहरूका लागि मात्र"),  # Only for ward officers
    )

    # Profile information
    profile_picture = models.ImageField(
        upload_to="users/profiles/",
        blank=True,
        null=True,
        verbose_name=_("प्रोफाइल फोटो"),  # Profile Picture
    )

    # Security and audit fields
    is_verified = models.BooleanField(
        default=False, verbose_name=_("प्रमाणित")  # Verified
    )

    last_password_change = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("अन्तिम पासवर्ड परिवर्तन"),  # Last Password Change
    )

    failed_login_attempts = models.IntegerField(
        default=0, verbose_name=_("असफल लगइन प्रयासहरू")  # Failed Login Attempts
    )

    account_locked_until = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("खाता लक गरिएको मिति"),  # Account Locked Until
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("सिर्जना मिति")  # Created Date
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("अपडेट मिति")  # Updated Date
    )

    class Meta:
        verbose_name = _("प्रयोगकर्ता")  # User
        verbose_name_plural = _("प्रयोगकर्ताहरू")  # Users
        ordering = ["-created_at"]

        # Permissions
        permissions = [
            ("can_manage_demographics", "Can manage demographic data"),
            ("can_manage_economics", "Can manage economic data"),
            ("can_manage_social", "Can manage social data"),
            ("can_manage_environment", "Can manage environment data"),
            ("can_manage_infrastructure", "Can manage infrastructure data"),
            ("can_manage_governance", "Can manage governance data"),
            ("can_generate_reports", "Can generate reports"),
            ("can_export_data", "Can export data"),
            ("can_manage_users", "Can manage users"),
        ]

    def __str__(self):
        """String representation of the user"""
        if self.full_name_nepali:
            return f"{self.full_name_nepali} ({self.username})"
        return self.username

    def get_full_name(self):
        """
        Return the full name in Nepali if available, otherwise English
        """
        if self.full_name_nepali:
            return self.full_name_nepali
        return super().get_full_name()

    def is_admin(self):
        """Check if user is administrator"""
        return self.role == self.UserRole.ADMIN

    def is_manager(self):
        """Check if user is manager"""
        return self.role == self.UserRole.MANAGER

    def is_ward_officer(self):
        """Check if user is ward officer"""
        return self.role == self.UserRole.WARD_OFFICER

    def can_edit_ward_data(self, ward_number):
        """Check if user can edit data for specific ward"""
        if self.is_admin() or self.is_manager():
            return True
        if self.is_ward_officer() and self.ward_number == ward_number:
            return True
        return False

    def is_account_locked(self):
        """Check if account is currently locked"""
        from django.utils import timezone

        if self.account_locked_until:
            return timezone.now() < self.account_locked_until
        return False

    def reset_failed_login_attempts(self):
        """Reset failed login attempts counter"""
        self.failed_login_attempts = 0
        self.account_locked_until = None
        self.save(update_fields=["failed_login_attempts", "account_locked_until"])

    def increment_failed_login_attempts(self):
        """Increment failed login attempts and lock account if needed"""
        from django.utils import timezone
        from datetime import timedelta

        self.failed_login_attempts += 1

        # Lock account after 5 failed attempts for 30 minutes
        if self.failed_login_attempts >= 5:
            self.account_locked_until = timezone.now() + timedelta(minutes=30)

        self.save(update_fields=["failed_login_attempts", "account_locked_until"])


class UserSession(models.Model):
    """
    Track user sessions for security auditing
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sessions",
        verbose_name=_("प्रयोगकर्ता"),  # User
    )

    session_key = models.CharField(
        max_length=40, verbose_name=_("सेसन कुञ्जी")  # Session Key
    )

    ip_address = models.GenericIPAddressField(verbose_name=_("IP ठेगाना"))  # IP Address

    user_agent = models.TextField(
        blank=True, verbose_name=_("प्रयोगकर्ता एजेन्ट")  # User Agent
    )

    login_time = models.DateTimeField(
        auto_now_add=True, verbose_name=_("लगइन समय")  # Login Time
    )

    logout_time = models.DateTimeField(
        blank=True, null=True, verbose_name=_("लगआउट समय")  # Logout Time
    )

    is_active = models.BooleanField(default=True, verbose_name=_("सक्रिय"))  # Active

    class Meta:
        verbose_name = _("प्रयोगकर्ता सेसन")  # User Session
        verbose_name_plural = _("प्रयोगकर्ता सेसनहरू")  # User Sessions
        ordering = ["-login_time"]

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"
