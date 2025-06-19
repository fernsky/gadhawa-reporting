"""
Chart Management Management Commands

Provides command-line utilities for chart management.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.chart_management.services import get_chart_service


class Command(BaseCommand):
    """Clean up old chart files and database entries"""

    help = "Clean up old unused chart files and database entries"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="Number of days to keep charts (default: 30)",
        )

        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be deleted without actually deleting",
        )

    def handle(self, *args, **options):
        days = options["days"]
        dry_run = options["dry_run"]

        self.stdout.write(
            self.style.SUCCESS(f"Cleaning up charts older than {days} days...")
        )

        if dry_run:
            self.stdout.write(
                self.style.WARNING("DRY RUN MODE - No files will be deleted")
            )

        chart_service = get_chart_service()

        if not dry_run:
            deleted_count = chart_service.cleanup_old_charts(days)
            self.stdout.write(
                self.style.SUCCESS(f"Cleaned up {deleted_count} old charts")
            )
        else:
            # For dry run, just show stats
            stats = chart_service.get_chart_stats()
            self.stdout.write(f"Total charts: {stats['total_charts']}")
            self.stdout.write(f"Completed charts: {stats['completed_charts']}")
            self.stdout.write(f"Failed charts: {stats['failed_charts']}")
            self.stdout.write(f"Cache hit rate: {stats['cache_hit_rate']}%")
