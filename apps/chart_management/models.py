"""
Simple Chart File Tracker

Minimal system to track chart files and their content hashes.
"""

import hashlib
from pathlib import Path
from django.db import models
from django.conf import settings
from apps.core.models import BaseModel


class ChartFile(BaseModel):
    """Simple chart file tracker"""

    # Basic identification
    chart_key = models.CharField(max_length=255, unique=True)
    chart_type = models.CharField(max_length=20)  # pie, bar, line, etc.

    # Content tracking
    content_hash = models.CharField(max_length=64)

    # File path (relative to charts directory)
    file_path = models.CharField(max_length=500)

    # Simple metadata
    title = models.CharField(max_length=255, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["chart_key"]),
            models.Index(fields=["content_hash"]),
        ]

    def __str__(self):
        return f"{self.chart_key} ({self.chart_type})"

    @property
    def full_path(self):
        """Get full filesystem path"""
        # Use same directory structure as chart service
        if hasattr(settings, "STATICFILES_DIRS") and settings.STATICFILES_DIRS:
            return (
                Path(settings.STATICFILES_DIRS[0])
                / "images"
                / "charts"
                / self.file_path
            )
        else:
            return Path(settings.STATIC_ROOT) / "images" / "charts" / self.file_path

    @property
    def url(self):
        """Get URL for the file"""
        if self.exists():
            return f"{settings.STATIC_URL}images/charts/{self.file_path}"
        return None

    def exists(self):
        """Check if file exists on filesystem"""
        return self.full_path.exists() if self.file_path else False

    @staticmethod
    def generate_content_hash(data):
        """Generate hash from data"""
        content_str = str(sorted(data.items())) if isinstance(data, dict) else str(data)
        return hashlib.sha256(content_str.encode("utf-8")).hexdigest()
