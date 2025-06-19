"""
Chart Management Signals

Handles cleanup and maintenance of chart files.
"""

from django.db.models.signals import post_delete
from django.dispatch import receiver
from pathlib import Path
from .models import ChartCache


@receiver(post_delete, sender=ChartCache)
def cleanup_chart_files(sender, instance, **kwargs):
    """Clean up chart files when ChartCache is deleted"""

    try:
        # Delete SVG file
        if instance.svg_path:
            svg_path = instance.get_svg_full_path()
            if svg_path and svg_path.exists():
                svg_path.unlink()

        # Delete PNG file
        if instance.png_path:
            png_path = instance.get_png_full_path()
            if png_path and png_path.exists():
                png_path.unlink()

    except Exception as e:
        print(f"Error cleaning up chart files for {instance.chart_key}: {e}")
