#!/usr/bin/env python
"""
Test ward settlement template rendering
"""

import os
import sys
import django

# Add the project directory to the path
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/gadhawa/gadhawa-report"
)

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gadhawa_report.settings.development")
django.setup()

from django.template.loader import render_to_string
from apps.demographics.processors.ward_settlement import WardSettlementProcessor


def test_template_rendering():
    """Test ward settlement template rendering"""
    processor = WardSettlementProcessor()

    print("=== Testing Ward Settlement Template ===")

    # Get processed data
    pdf_data = processor.process_for_pdf()

    # Prepare context like the PDF view does
    context = {
        "report_content": pdf_data["report_content"],
        "data": pdf_data["data"],
        "total_settlements": pdf_data["total_settlements"],
        "total_wards": pdf_data["total_wards"],
    }

    try:
        # Render the template
        html = render_to_string(
            "demographics/ward_settlement/ward_settlement_report_partial.html", context
        )

        print("✅ Template rendered successfully!")
        print(f"HTML length: {len(html)} characters")

        # Check if it contains the table structure
        if "तालिका ३.१.१" in html:
            print("✅ Table title found")
        else:
            print("❌ Table title not found")

        if "वडा नं." in html:
            print("✅ Table headers found")
        else:
            print("❌ Table headers not found")

        # Count ward rows (should be 7)
        ward_count = html.count('<td style="text-align: center; font-weight: bold;">')
        print(f"Ward rows found: {ward_count}")

        # Save a sample for inspection
        with open("/tmp/ward_settlement_test.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("✅ Sample HTML saved to /tmp/ward_settlement_test.html")

    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_template_rendering()
