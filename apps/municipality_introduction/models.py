"""
Municipality Introduction models for Gadhawa Rural Municipality Digital Profile

This module contains models related to municipality introduction information.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
import uuid


class BaseModel(models.Model):
    """Abstract base model with common fields"""

    id = models.CharField(
        max_length=36, primary_key=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PoliticalStatus(BaseModel):
    """Political status model for ward-wise population data"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        verbose_name=_("वडा नं."),
    )
    ward_name = models.CharField(max_length=200, verbose_name=_("वडाको नाम"))
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(2070), MaxValueValidator(2090)],
        verbose_name=_("वर्ष"),
    )
    population = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], verbose_name=_("जनसंख्या")
    )

    class Meta:
        verbose_name = _("राजनैतिक अवस्था")
        verbose_name_plural = _("राजनैतिक अवस्थाहरू")
        unique_together = ["ward_number", "year"]
        ordering = ["ward_number", "year"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.ward_name} ({self.year})"
