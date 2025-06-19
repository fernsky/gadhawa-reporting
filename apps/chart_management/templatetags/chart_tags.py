"""
Chart Management Template Tags

Provides template tags for easy chart generation and display.
"""

from django import template
from django.utils.safestring import mark_safe
from ..services import get_chart_service

register = template.Library()


@register.simple_tag
def chart_image(chart_key, chart_type, data, title, width=800, height=400, **kwargs):
    """
    Generate and display chart image
    
    Usage:
        {% chart_image "demographics_religion" "pie" religion_data "धर्म अनुसार जनसंख्या" width=900 height=450 %}
    """
    
    chart_service = get_chart_service()
    
    svg_url, png_url = chart_service.get_or_generate_chart(
        chart_key=chart_key,
        chart_type=chart_type,
        data=data,
        title=title,
        width=width,
        height=height,
        **kwargs
    )
    
    if png_url:
        # Prefer PNG for better compatibility
        return mark_safe(
            f'<img src="{png_url}" alt="{title}" class="chart-image" '
            f'style="width: {width}px; height: {height}px;" />'
        )
    elif svg_url:
        # Fallback to SVG
        return mark_safe(
            f'<img src="{svg_url}" alt="{title}" class="chart-image" '
            f'style="width: {width}px; height: {height}px;" />'
        )
    else:
        # Error placeholder
        return mark_safe(
            f'<div class="chart-error" style="width: {width}px; height: {height}px; '
            f'border: 2px dashed #ccc; display: flex; align-items: center; '
            f'justify-content: center; color: #666;">'
            f'चार्ट लोड गर्न सकिएन: {title}</div>'
        )


@register.simple_tag
def chart_svg_url(chart_key, chart_type, data, title, width=800, height=400, **kwargs):
    """
    Get SVG URL for chart
    
    Usage:
        {% chart_svg_url "demographics_religion" "pie" religion_data "धर्म अनुसार जनसंख्या" as svg_url %}
    """
    
    chart_service = get_chart_service()
    
    svg_url, _ = chart_service.get_or_generate_chart(
        chart_key=chart_key,
        chart_type=chart_type,
        data=data,
        title=title,
        width=width,
        height=height,
        **kwargs
    )
    
    return svg_url or ""


@register.simple_tag
def chart_png_url(chart_key, chart_type, data, title, width=800, height=400, **kwargs):
    """
    Get PNG URL for chart
    
    Usage:
        {% chart_png_url "demographics_religion" "pie" religion_data "धर्म अनुसार जनसंख्या" as png_url %}
    """
    
    chart_service = get_chart_service()
    
    _, png_url = chart_service.get_or_generate_chart(
        chart_key=chart_key,
        chart_type=chart_type,
        data=data,
        title=title,
        width=width,
        height=height,
        **kwargs
    )
    
    return png_url or ""


@register.inclusion_tag('chart_management/chart_with_fallback.html')
def chart_with_fallback(chart_key, chart_type, data, title, width=800, height=400, **kwargs):
    """
    Render chart with fallback options
    
    Usage:
        {% chart_with_fallback "demographics_religion" "pie" religion_data "धर्म अनुसार जनसंख्या" width=900 height=450 %}
    """
    
    chart_service = get_chart_service()
    
    svg_url, png_url = chart_service.get_or_generate_chart(
        chart_key=chart_key,
        chart_type=chart_type,
        data=data,
        title=title,
        width=width,
        height=height,
        **kwargs
    )
    
    return {
        'svg_url': svg_url,
        'png_url': png_url,
        'title': title,
        'width': width,
        'height': height,
        'chart_key': chart_key,
    }


@register.simple_tag
def chart_stats():
    """
    Get chart generation statistics
    
    Usage:
        {% chart_stats as stats %}
    """
    
    chart_service = get_chart_service()
    return chart_service.get_chart_stats()
