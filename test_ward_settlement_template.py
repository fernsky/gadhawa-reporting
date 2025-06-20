#!/usr/bin/env python
"""
Test ward settlement HTML template rendering
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
from apps.demographics.processors.ward_settlement import WardSettlementProcessor


def test_template_rendering():
    print("🧪 Testing Ward Settlement Template Rendering...")

    # Get processor and data
    processor = WardSettlementProcessor()
    pdf_data = processor.process_for_pdf()

    # Get template
    try:
        template = get_template(
            "demographics/ward_settlement/ward_settlement_report_partial.html"
        )
        print("✅ Template loaded successfully")
    except Exception as e:
        print(f"❌ Template loading failed: {e}")
        return

    # Prepare context data
    report_content = pdf_data["report_content"]
    context_data = {
        "coherent_analysis": report_content["coherent_analysis"],
        "ward_data": report_content["ward_data"],
        "total_settlements": pdf_data["total_settlements"],
        "total_wards": pdf_data["total_wards"],
    }

    # Render template
    try:
        rendered_html = template.render(context_data)
        print("✅ Template rendered successfully")
        print(f"   HTML length: {len(rendered_html)} characters")

        # Check if key content is present
        if "मुख्य बस्ती र घरपरिवारको विवरण" in rendered_html:
            print("✅ Section title found in HTML")
        if "तालिका ३.१.१" in rendered_html:
            print("✅ Table title found in HTML")
        if "वडा नं." in rendered_html:
            print("✅ Ward number header found in HTML")

        # Check for specific settlements
        settlement_checks = ["पाङ", "खालावस्ती", "जुतुङखोला"]
        found_settlements = [s for s in settlement_checks if s in rendered_html]
        print(
            f"✅ Found {len(found_settlements)}/{len(settlement_checks)} sample settlements"
        )

    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        return

    print("✅ Ward Settlement Template test completed successfully!")


if __name__ == "__main__":
    test_template_rendering()
