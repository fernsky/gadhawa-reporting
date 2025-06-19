"""
Simple Chart File Service

Basic service for tracking chart files with minimal overhead.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from django.conf import settings
from .models import ChartFile


class SimpleChartService:
    """Simple chart file tracking service"""

    def __init__(self):
        self.charts_dir = Path(settings.STATICFILES_DIRS[0]) / "images" / "charts"
        self.charts_dir.mkdir(parents=True, exist_ok=True)

    def track_chart(
        self,
        chart_key: str,
        chart_type: str,
        data: Dict[str, Any],
        file_path: str,
        title: str = "",
    ) -> Optional[str]:
        """
        Track a chart file

        Args:
            chart_key: Unique identifier for the chart
            chart_type: Type of chart (pie, bar, etc.)
            data: Chart data for hash generation
            file_path: Relative path to the chart file
            title: Optional title

        Returns:
            URL of the chart file if it exists, None otherwise
        """

        content_hash = ChartFile.generate_content_hash(data)

        # Check if we already have this chart
        try:
            chart_file = ChartFile.objects.get(chart_key=chart_key)

            # If content hasn't changed and file exists, return URL
            if chart_file.content_hash == content_hash and chart_file.exists():
                return chart_file.url

            # Update if content changed
            chart_file.content_hash = content_hash
            chart_file.file_path = file_path
            chart_file.title = title
            chart_file.save()

        except ChartFile.DoesNotExist:
            # Create new record
            chart_file = ChartFile.objects.create(
                chart_key=chart_key,
                chart_type=chart_type,
                content_hash=content_hash,
                file_path=file_path,
                title=title,
            )

        # Return URL if file exists
        return chart_file.url if chart_file.exists() else None

    def get_chart_url(self, chart_key: str) -> Optional[str]:
        """Get URL for existing chart"""
        try:
            chart_file = ChartFile.objects.get(chart_key=chart_key)
            return chart_file.url if chart_file.exists() else None
        except ChartFile.DoesNotExist:
            return None

    def is_chart_current(self, chart_key: str, data: Dict[str, Any]) -> bool:
        """Check if chart is current (data hasn't changed)"""
        try:
            chart_file = ChartFile.objects.get(chart_key=chart_key)
            content_hash = ChartFile.generate_content_hash(data)
            return chart_file.content_hash == content_hash and chart_file.exists()
        except ChartFile.DoesNotExist:
            return False

    def cleanup_missing_files(self) -> int:
        """Remove records for files that don't exist"""
        count = 0
        for chart_file in ChartFile.objects.all():
            if not chart_file.exists():
                chart_file.delete()
                count += 1
        return count


# Global service instance
_chart_service = None


def get_chart_service() -> SimpleChartService:
    """Get the global chart service instance"""
    global _chart_service
    if _chart_service is None:
        _chart_service = SimpleChartService()
    return _chart_service
