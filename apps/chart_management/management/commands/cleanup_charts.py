"""
Simple Chart Cleanup Command

Clean up chart file entries for missing files.
"""

from django.core.management.base import BaseCommand
from apps.chart_management.services import get_chart_service


class Command(BaseCommand):
    """Clean up chart entries for missing files"""

    help = "Remove chart entries for files that no longer exist"

    def handle(self, *args, **options):
        self.stdout.write("Cleaning up missing chart files...")

        chart_service = get_chart_service()
        deleted_count = chart_service.cleanup_missing_files()

        self.stdout.write(
            self.style.SUCCESS(f"Removed {deleted_count} entries for missing files")
        )
