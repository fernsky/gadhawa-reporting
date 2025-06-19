"""
Simple Chart Template Tags

Basic template tags for chart file display.
"""

from django import template
from django.utils.safestring import mark_safe
from ..services import get_chart_service

register = template.Library()


@register.simple_tag
def chart_url(chart_key):
    """
    Get chart URL by key

    Usage:
        {% chart_url "demographics_religion_pie" as chart_url %}
        {% if chart_url %}<img src="{{ chart_url }}" alt="Chart" />{% endif %}
    """
    chart_service = get_chart_service()
    return chart_service.get_chart_url(chart_key) or ""


@register.simple_tag
def chart_image(chart_key, alt_text="Chart", css_class="chart-image"):
    """
    Display chart image with fallback

    Usage:
        {% chart_image "demographics_religion_pie" "Religion Distribution" "pie-chart" %}
    """
    chart_service = get_chart_service()
    url = chart_service.get_chart_url(chart_key)

    if url:
        return mark_safe(f'<img src="{url}" alt="{alt_text}" class="{css_class}" />')
    else:
        return mark_safe(
            f'<div class="chart-placeholder {css_class}">चार्ट उपलब्ध छैन: {alt_text}</div>'
        )
