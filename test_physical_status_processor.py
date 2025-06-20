#!/usr/bin/env python
"""
Test script for physical status processor
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

from apps.municipality_introduction.processors.physical_status import (
    PhysicalStatusProcessor,
)


def test_physical_status_processor():
    print("🧪 Testing Physical Status Processor...")

    processor = PhysicalStatusProcessor()

    # Test basic attributes
    print(f"Section Title: {processor.get_section_title()}")
    print(f"Section Number: {processor.get_section_number()}")

    # Test data retrieval
    data = processor.get_data()
    print(f"\nData Summary:")
    print(f"Municipality: {data.get('municipality_name', 'N/A')}")
    print(f"Province: {data.get('province_name', 'N/A')}")
    print(f"District: {data.get('district_name', 'N/A')}")
    print(f"Area: {data.get('total_area_sq_km', 0)} sq km")
    print(f"Population: {data.get('total_population', 0):,}")
    print(f"Headquarters: {data.get('headquarters_location', 'N/A')}")

    # Test report generation
    report_content = processor.generate_report_content(data)
    print(
        f"\nReport Generated: {len(report_content.get('coherent_analysis', ''))} characters"
    )

    # Test PDF processing
    pdf_data = processor.process_for_pdf()
    print(f"\nPDF Data Keys: {list(pdf_data.keys())}")

    print("✅ Physical Status Processor test completed successfully!")


if __name__ == "__main__":
    test_physical_status_processor()
