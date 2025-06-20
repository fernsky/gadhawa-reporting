#!/usr/bin/env python
"""
Test physical status HTML template rendering
"""
import os
import sys
import django

# Setup Django
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from django.template.loader import get_template
from django.template import Context
from apps.municipality_introduction.processors.physical_status import (
    PhysicalStatusProcessor,
)


def test_template_rendering():
    print("🧪 Testing Physical Status Template Rendering...")

    # Get processor and data
    processor = PhysicalStatusProcessor()
    pdf_data = processor.process_for_pdf()

    # Get template
    try:
        template = get_template(
            "municipality_introduction/physical_status/physical_status_report_partial.html"
        )
        print("✅ Template loaded successfully")
    except Exception as e:
        print(f"❌ Template loading failed: {e}")
        return

    # Prepare context data
    report_content = pdf_data["report_content"]
    context_data = {
        "coherent_analysis": report_content["coherent_analysis"],
        "basic_info": report_content["basic_info"],
        "geographical_info": report_content["geographical_info"],
        "climate_info": report_content["climate_info"],
    }

    # Render template
    try:
        rendered_html = template.render(context_data)
        print("✅ Template rendered successfully")
        print(f"   HTML length: {len(rendered_html)} characters")

        # Check if key content is present
        if "भौगोलिक अवस्थिति" in rendered_html:
            print("✅ Section title found in HTML")
        if "तालिका २.१.१" in rendered_html:
            print("✅ Table title found in HTML")
        if "लुङ्ग्री गाउँपालिका" in rendered_html:
            print("✅ Municipality name found in HTML")

        # Check for specific data
        data_checks = ["लुम्बिनी प्रदेश", "रोल्पा", "किलाचौर"]
        found_data = [d for d in data_checks if d in rendered_html]
        print(f"✅ Found {len(found_data)}/{len(data_checks)} key data items")

    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        return

    print("✅ Physical Status Template test completed successfully!")


if __name__ == "__main__":
    test_template_rendering()
