"""
Simple Chart File Admin

Minimal admin interface for chart file tracking.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import ChartFile


@admin.register(ChartFile)
class ChartFileAdmin(admin.ModelAdmin):
    """Simple admin for chart files"""

    list_display = [
        "chart_key",
        "chart_type", 
        "title",
        "file_exists",
        "created_at",
    ]

    list_filter = [
        "chart_type",
        "created_at",
    ]

    search_fields = ["chart_key", "title"]

    readonly_fields = [
        "content_hash",
        "created_at",
        "updated_at",
        "file_preview",
    ]

    fieldsets = (
        ("Basic Info", {
            "fields": ("chart_key", "chart_type", "title")
        }),
        ("File Info", {
            "fields": ("file_path", "content_hash")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
        ("Preview", {
            "fields": ("file_preview",)
        }),
    )

    def file_exists(self, obj):
        """Show if file exists"""
        return "✅" if obj.exists() else "❌"
    file_exists.short_description = "File Exists"
    file_exists.boolean = True

    def file_preview(self, obj):
        """Show file preview"""
        if obj.url:
            return format_html(
                '<img src="{}" alt="{}" style="max-width: 300px; max-height: 200px;" />',
                obj.url,
                obj.title or obj.chart_key,
            )
        return "No preview available"
    file_preview.short_description = "Preview"

    actions = ["cleanup_missing_files"]

    def cleanup_missing_files(self, request, queryset):
        """Remove entries for missing files"""
        count = 0
        for chart_file in queryset:
            if not chart_file.exists():
                chart_file.delete()
                count += 1
        
        self.message_user(request, f"Removed {count} entries for missing files.")
    cleanup_missing_files.short_description = "Remove entries for missing files"
