#!/usr/bin/env python
"""
Test script for ward settlement processor
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

from apps.demographics.processors.ward_settlement import WardSettlementProcessor


def test_ward_settlement_processor():
    print("🧪 Testing Ward Settlement Processor...")

    processor = WardSettlementProcessor()

    # Test basic attributes
    print(f"Section Title: {processor.get_section_title()}")
    print(f"Section Number: {processor.get_section_number()}")
    print(f"Subsection Title: {processor.get_subsection_title()}")
    print(f"Subsection Number: {processor.get_subsection_number()}")

    # Test data retrieval
    data = processor.get_data()
    print(f"\nData Summary:")
    print(f"Total Wards: {data.get('total_wards', 0)}")
    print(f"Total Settlements: {data.get('total_settlements', 0)}")

    # Test ward data
    ward_data = data.get("ward_data", {})
    print(f"\nWard-wise Data:")
    for ward_num, ward_info in ward_data.items():
        settlement_count = len(ward_info.get("settlement_areas", []))
        print(f"  Ward {ward_num}: {settlement_count} settlements")

    # Test report generation
    report_content = processor.generate_report_content(data)
    print(
        f"\nReport Generated: {len(report_content.get('coherent_analysis', ''))} characters"
    )

    # Test PDF processing
    pdf_data = processor.process_for_pdf()
    print(f"\nPDF Data Keys: {list(pdf_data.keys())}")

    print("✅ Ward Settlement Processor test completed successfully!")


if __name__ == "__main__":
    test_ward_settlement_processor()
