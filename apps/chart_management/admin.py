"""
Chart Management Admin

Admin interface for managing chart cache and generation logs.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import ChartCache, ChartGenerationLog


@admin.register(ChartCache)
class ChartCacheAdmin(admin.ModelAdmin):
    """Admin for Chart Cache"""
    
    list_display = [
        'chart_key', 
        'chart_type', 
        'status', 
        'title', 
        'width', 
        'height',
        'access_count',
        'chart_preview',
        'created_at'
    ]
    
    list_filter = [
        'chart_type', 
        'status', 
        'created_at',
        'svg_generated_at',
        'png_generated_at'
    ]
    
    search_fields = [
        'chart_key', 
        'title', 
        'content_hash'
    ]
    
    readonly_fields = [
        'content_hash',
        'svg_content_hash', 
        'svg_generated_at',
        'png_generated_at',
        'access_count',
        'last_accessed',
        'chart_preview',
        'file_status'
    ]
    
    fieldsets = (
        ('Chart Information', {
            'fields': ('chart_key', 'chart_type', 'title', 'status')
        }),
        ('Dimensions', {
            'fields': ('width', 'height')
        }),
        ('Content Tracking', {
            'fields': ('content_hash', 'svg_content_hash')
        }),
        ('File Paths', {
            'fields': ('svg_path', 'png_path', 'file_status')
        }),
        ('Generation Info', {
            'fields': ('svg_generated_at', 'png_generated_at', 'error_message')
        }),
        ('Usage Statistics', {
            'fields': ('access_count', 'last_accessed')
        }),
        ('Preview', {
            'fields': ('chart_preview',)
        })
    )
    
    def chart_preview(self, obj):
        """Show chart preview in admin"""
        if obj.png_url:
            return format_html(
                '<img src="{}" alt="{}" style="max-width: 200px; max-height: 150px;" />',
                obj.png_url,
                obj.title
            )
        elif obj.svg_url:
            return format_html(
                '<img src="{}" alt="{}" style="max-width: 200px; max-height: 150px;" />',
                obj.svg_url,
                obj.title
            )
        return "No preview available"
    
    chart_preview.short_description = "Preview"
    
    def file_status(self, obj):
        """Show file existence status"""
        svg_status = "✅" if obj.svg_exists() else "❌"
        png_status = "✅" if obj.png_exists() else "❌" if obj.png_path else "N/A"
        
        return format_html(
            "SVG: {} | PNG: {}",
            svg_status,
            png_status
        )
    
    file_status.short_description = "File Status"
    
    actions = ['cleanup_missing_files', 'regenerate_png']
    
    def cleanup_missing_files(self, request, queryset):
        """Clean up charts with missing files"""
        count = 0
        for chart in queryset:
            if not chart.svg_exists() or (chart.png_path and not chart.png_exists()):
                chart.status = 'failed'
                chart.error_message = "Files missing from filesystem"
                chart.save()
                count += 1
        
        self.message_user(request, f"Updated {count} charts with missing files.")
    
    cleanup_missing_files.short_description = "Mark charts with missing files as failed"
    
    def regenerate_png(self, request, queryset):
        """Regenerate PNG files for selected charts"""
        from .services import get_chart_service
        
        chart_service = get_chart_service()
        count = 0
        
        for chart in queryset:
            if chart.svg_exists():
                try:
                    svg_path = chart.get_svg_full_path()
                    png_path = chart_service._generate_png_file(chart, svg_path)
                    if png_path:
                        chart.png_path = png_path.name
                        chart.png_generated_at = timezone.now()
                        chart.save()
                        count += 1
                except Exception as e:
                    chart.error_message = f"PNG regeneration failed: {str(e)}"
                    chart.save()
        
        self.message_user(request, f"Regenerated PNG for {count} charts.")
    
    regenerate_png.short_description = "Regenerate PNG files"


@admin.register(ChartGenerationLog)
class ChartGenerationLogAdmin(admin.ModelAdmin):
    """Admin for Chart Generation Log"""
    
    list_display = [
        'chart_cache',
        'operation_type',
        'status',
        'processing_time',
        'created_at'
    ]
    
    list_filter = [
        'operation_type',
        'status',
        'created_at'
    ]
    
    search_fields = [
        'chart_cache__chart_key',
        'chart_cache__title'
    ]
    
    readonly_fields = [
        'chart_cache',
        'operation_type',
        'status',
        'processing_time',
        'error_message',
        'metadata',
        'created_at'
    ]
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
