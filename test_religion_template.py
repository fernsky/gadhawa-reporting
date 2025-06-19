#!/usr/bin/env python
"""
Test Religion Template Integration with Chart Management

This script tests the template integration with chart management system.
"""

import os
import django
from pathlib import Path

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from django.template import Context, Template
from apps.demographics.processors.religion import ReligionProcessor


def test_template_integration():
    """Test template integration with chart management"""
    print("=== Testing Template Integration ===\n")

    # Get religion data
    processor = ReligionProcessor()
    pdf_data = processor.process_for_pdf()

    # Test template with chart_tags
    template_content = """
    {% load chart_tags %}
    
    <!-- Test chart_url tag -->
    {% chart_url "demographics_religion_pie" as pie_chart_url %}
    Pie Chart URL: {{ pie_chart_url }}
    
    <!-- Test chart_image tag -->
    {% chart_image "demographics_religion_pie" "Religion Distribution" "religion-chart" %}
    
    <!-- Test with data from processor -->
    Charts from processor: {{ charts.pie_chart_url }}
    """

    template = Template(template_content)
    context = Context(
        {
            "charts": pdf_data["charts"],
            "religion_data": pdf_data["data"],
            "chart_management_status": pdf_data["chart_management_status"],
        }
    )

    try:
        rendered = template.render(context)
        print("✓ Template rendered successfully:")
        print(rendered)

        # Check if URLs are present
        if "/static/images/charts/religion_pie_chart.svg" in rendered:
            print("✓ Chart URLs are correctly rendered in template")
        else:
            print("⚠ Chart URLs not found in rendered template")

    except Exception as e:
        print(f"⚠ Template rendering error: {e}")

    print("\n=== Template Test Completed ===")


if __name__ == "__main__":
    test_template_integration()
