"""
Simple Chart File Service

Basic service for tracking chart files based on file existence only.
"""

from pathlib import Path
from typing import Optional
from django.conf import settings
from .models import ChartFile


class SimpleChartService:
    """Simple chart file tracking service - file existence based"""

    def __init__(self):
        self.charts_dir = Path(settings.STATICFILES_DIRS[0]) / "images" / "charts"
        self.charts_dir.mkdir(parents=True, exist_ok=True)

    def track_chart(
        self,
        chart_key: str,
        chart_type: str,
        file_path: str,
        title: str = "",
    ) -> Optional[str]:
        """
        Track a chart file - only creates record if file exists

        Args:
            chart_key: Unique identifier for the chart
            chart_type: Type of chart (pie, bar, etc.)
            file_path: Relative path to the chart file
            title: Optional title

        Returns:
            URL of the chart file if it exists, None otherwise
        """

        try:
            # Check if we already have this chart
            chart_file = ChartFile.objects.get(chart_key=chart_key)

            # If file exists, return URL
            if chart_file.exists():
                print(f"✓ Chart already exists: {chart_file.file_path}")
                return chart_file.url
            else:
                # File doesn't exist, update with new path
                chart_file.file_path = file_path
                chart_file.chart_type = chart_type
                chart_file.title = title
                chart_file.save()

                # Return URL only if file actually exists
                if chart_file.exists():
                    print(f"✓ Updated chart file: {chart_file.file_path}")
                    return chart_file.url
                else:
                    print(f"⚠ Chart file not found: {chart_file.file_path}")
                    return None

        except ChartFile.DoesNotExist:
            # Create new record
            chart_file = ChartFile.objects.create(
                chart_key=chart_key,
                chart_type=chart_type,
                file_path=file_path,
                title=title,
            )

            # Return URL only if file actually exists
            if chart_file.exists():
                print(f"✓ Tracked new chart: {chart_file.file_path}")
                return chart_file.url
            else:
                print(f"⚠ Chart file not found: {chart_file.file_path}")
                return None

    def chart_exists(self, chart_key: str) -> bool:
        """Check if chart exists (both in database and file system)"""
        try:
            chart_file = ChartFile.objects.get(chart_key=chart_key)
            return chart_file.exists()
        except ChartFile.DoesNotExist:
            return False

    def get_chart_url(self, chart_key: str) -> Optional[str]:
        """Get URL for existing chart"""
        try:
            chart_file = ChartFile.objects.get(chart_key=chart_key)
            return chart_file.url if chart_file.exists() else None
        except ChartFile.DoesNotExist:
            return None

    def needs_generation(self, chart_key: str) -> bool:
        """Check if chart needs to be generated (doesn't exist)"""
        return not self.chart_exists(chart_key)

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
