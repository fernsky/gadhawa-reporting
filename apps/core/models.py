"""
Base models for Gadhawa Report System.

This module contains abstract base models that provide common functionality
for other models in the system.
"""

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class BaseModel(models.Model):
    """
    Abstract base model that provides common fields for all models
    """
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('सिर्जना मिति')  # Created Date
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('अपडेट मिति')  # Updated Date
    )
    
    created_by = models.ForeignKey(
        'users.User',  # String reference to avoid circular import
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created',
        verbose_name=_('सिर्जनाकर्ता')  # Creator
    )
    
    updated_by = models.ForeignKey(
        'users.User',  # String reference to avoid circular import
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated',
        verbose_name=_('अपडेटकर्ता')  # Updater
    )
    
    class Meta:
        abstract = True
        ordering = ['-created_at']


class WardModel(BaseModel):
    """
    Abstract base model for models that have ward-specific data
    """
    
    ward_number = models.IntegerField(
        verbose_name=_('वडा नं'),  # Ward Number
        help_text=_('गढवा गाउँपालिकाको वडा नम्बर (१-८)')  # Ward number of Gadhawa Rural Municipality (1-8)
    )
    
    class Meta:
        abstract = True
        ordering = ['ward_number', '-created_at']


class ReportSectionModel(BaseModel):
    """
    Abstract base model for report section models
    """
    
    section_name = models.CharField(
        max_length=100,
        verbose_name=_('खण्डको नाम')  # Section Name
    )
    
    section_name_english = models.CharField(
        max_length=100,
        verbose_name=_('खण्डको नाम (अंग्रेजीमा)')  # Section Name in English
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('सक्रिय')  # Active
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name=_('क्रम')  # Order
    )
    
    class Meta:
        abstract = True
        ordering = ['order', 'section_name']
