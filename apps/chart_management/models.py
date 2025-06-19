"""
Chart Management Models

Tracks generated charts, their hashes, and provides efficient caching.
"""

import hashlib
import os
from pathlib import Path
from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel


class ChartTypeChoice(models.TextChoices):
    """Chart type choices"""

    PIE = "pie", _("पाई चार्ट")
    BAR = "bar", _("बार चार्ट")
    LINE = "line", _("लाइन चार्ट")
    DONUT = "donut", _("डोनट चार्ट")


class ChartStatusChoice(models.TextChoices):
    """Chart generation status choices"""

    PENDING = "pending", _("पेन्डिङ")
    GENERATING = "generating", _("जेनेरेट हुँदै")
    COMPLETED = "completed", _("पूरा भयो")
    FAILED = "failed", _("असफल")


class ChartCache(BaseModel):
    """
    Model to track generated charts and provide efficient caching
    """

    # Chart identification
    chart_key = models.CharField(
        max_length=255,
        verbose_name=_("चार्ट की"),
        help_text=_("Unique identifier for the chart"),
    )

    chart_type = models.CharField(
        max_length=20, choices=ChartTypeChoice.choices, verbose_name=_("चार्ट प्रकार")
    )

    # Content tracking
    content_hash = models.CharField(
        max_length=64,
        verbose_name=_("कन्टेन्ट ह्यास"),
        help_text=_("SHA-256 hash of the chart data"),
    )

    svg_content_hash = models.CharField(
        max_length=64,
        verbose_name=_("SVG कन्टेन्ट ह्यास"),
        help_text=_("SHA-256 hash of the generated SVG content"),
    )

    # File paths
    svg_path = models.CharField(
        max_length=500,
        verbose_name=_("SVG फाइल पथ"),
        help_text=_("Relative path to the SVG file"),
    )

    png_path = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_("PNG फाइल पथ"),
        help_text=_("Relative path to the PNG file"),
    )

    # Generation status
    status = models.CharField(
        max_length=20,
        choices=ChartStatusChoice.choices,
        default=ChartStatusChoice.PENDING,
        verbose_name=_("स्थिति"),
    )

    # Metadata
    title = models.CharField(max_length=255, verbose_name=_("शीर्षक"))

    width = models.IntegerField(verbose_name=_("चौडाइ"))

    height = models.IntegerField(verbose_name=_("उचाइ"))

    # Processing info
    svg_generated_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("SVG जेनेरेशन समय")
    )

    png_generated_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("PNG जेनेरेशन समय")
    )

    error_message = models.TextField(blank=True, null=True, verbose_name=_("त्रुटि सन्देश"))

    # Usage tracking
    access_count = models.IntegerField(default=0, verbose_name=_("पहुँच गणना"))

    last_accessed = models.DateTimeField(
        null=True, blank=True, verbose_name=_("अन्तिम पहुँच")
    )

    class Meta:
        verbose_name = _("चार्ट क्यास")
        verbose_name_plural = _("चार्ट क्यासहरू")
        unique_together = ["chart_key", "content_hash"]
        indexes = [
            models.Index(fields=["chart_key"]),
            models.Index(fields=["content_hash"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.chart_key} - {self.get_chart_type_display()}"

    @property
    def svg_url(self):
        """Get the URL for the SVG file"""
        if self.svg_path and self.svg_exists():
            return f"{settings.STATIC_URL}images/charts/{self.svg_path}"
        return None

    @property
    def png_url(self):
        """Get the URL for the PNG file"""
        if self.png_path and self.png_exists():
            return f"{settings.STATIC_URL}images/charts/{self.png_path}"
        return None

    def svg_exists(self):
        """Check if SVG file exists"""
        if not self.svg_path:
            return False
        full_path = Path(settings.STATIC_ROOT) / "images" / "charts" / self.svg_path
        return full_path.exists()

    def png_exists(self):
        """Check if PNG file exists"""
        if not self.png_path:
            return False
        full_path = Path(settings.STATIC_ROOT) / "images" / "charts" / self.png_path
        return full_path.exists()

    def get_svg_full_path(self):
        """Get full filesystem path for SVG"""
        if not self.svg_path:
            return None
        return Path(settings.STATIC_ROOT) / "images" / "charts" / self.svg_path

    def get_png_full_path(self):
        """Get full filesystem path for PNG"""
        if not self.png_path:
            return None
        return Path(settings.STATIC_ROOT) / "images" / "charts" / self.png_path

    @staticmethod
    def generate_content_hash(data):
        """Generate SHA-256 hash from chart data"""
        if isinstance(data, dict):
            # Sort keys for consistent hashing
            content_str = str(sorted(data.items()))
        else:
            content_str = str(data)

        return hashlib.sha256(content_str.encode("utf-8")).hexdigest()

    @staticmethod
    def generate_svg_content_hash(svg_content):
        """Generate SHA-256 hash from SVG content"""
        return hashlib.sha256(svg_content.encode("utf-8")).hexdigest()

    def mark_accessed(self):
        """Mark chart as accessed and increment counter"""
        from django.utils import timezone

        self.access_count += 1
        self.last_accessed = timezone.now()
        self.save(update_fields=["access_count", "last_accessed"])


class ChartGenerationLog(BaseModel):
    """
    Log of chart generation attempts and results
    """

    chart_cache = models.ForeignKey(
        ChartCache,
        on_delete=models.CASCADE,
        related_name="generation_logs",
        verbose_name=_("चार्ट क्यास"),
    )

    operation_type = models.CharField(
        max_length=20,
        choices=[
            ("svg_generation", _("SVG जेनेरेशन")),
            ("png_conversion", _("PNG रूपान्तरण")),
            ("cleanup", _("सफाई")),
        ],
        verbose_name=_("अपरेशन प्रकार"),
    )

    status = models.CharField(
        max_length=20, choices=ChartStatusChoice.choices, verbose_name=_("स्थिति")
    )

    processing_time = models.FloatField(
        null=True, blank=True, verbose_name=_("प्रोसेसिङ समय (सेकेन्ड)")
    )

    error_message = models.TextField(blank=True, null=True, verbose_name=_("त्रुटि सन्देश"))

    metadata = models.JSONField(default=dict, blank=True, verbose_name=_("मेटाडेटा"))

    class Meta:
        verbose_name = _("चार्ट जेनेरेशन लग")
        verbose_name_plural = _("चार्ट जेनेरेशन लगहरू")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.chart_cache.chart_key} - {self.operation_type} - {self.status}"
