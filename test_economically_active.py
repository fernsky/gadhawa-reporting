#!/usr/bin/env python3
"""
Test script for economically active processor
"""
import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.demographics.processors.economically_active import EconomicallyActiveProcessor


def test_economically_active():
    print("Testing EconomicallyActiveProcessor...")

    try:
        processor = EconomicallyActiveProcessor()
        print("✓ Processor initialized successfully")

        # Test get_data
        data = processor.get_data()
        print(f"✓ Data retrieved successfully")
        print(f"  - Total population: {data.get('total_population', 0)}")
        print(f"  - Age groups: {len(data.get('age_group_data', {}))}")
        print(f"  - Ward data: {len(data.get('ward_data', {}))}")

        # Test chart key
        chart_key = processor.get_chart_key()
        print(f"✓ Chart key: {chart_key}")

        # Test report generation
        report_content = processor.generate_report_content(data)
        print(f"✓ Report content generated: {len(report_content)} characters")

        # Test PDF processing
        pdf_data = processor.process_for_pdf()
        print("✓ PDF processing successful")
        print(f"  - Charts available: {'charts' in pdf_data}")
        print(f"  - Report content: {'report_content' in pdf_data}")

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_economically_active()
    if success:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Tests failed!")
