#!/usr/bin/env python
"""
Test script for death registration processor
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gadhawa_report.settings.development")
django.setup()

from apps.demographics.processors.death_registration import DeathRegistrationProcessor
from apps.demographics.processors.manager import DemographicsManager


def test_death_registration():
    """Test death registration processor"""
    print("🧪 Testing Death Registration Processor...")

    # Create processor
    processor = DeathRegistrationProcessor()

    # Get data
    data = processor.get_data()
    print(f"✅ Data retrieved successfully")
    print(f"   Total deaths: {data['total_deaths']}")
    print(
        f"   Age groups with deaths: {len([k for k, v in data['municipality_data'].items() if v['total'] > 0])}"
    )

    # Test report generation
    report_content = processor.generate_report_content(data)
    print(f"✅ Report content generated ({len(report_content)} characters)")

    # Test chart generation
    print("🔄 Generating charts...")
    charts = processor.generate_and_track_charts(data)
    print(f"✅ Charts generated: {list(charts.keys())}")

    # Test PDF processing
    pdf_data = processor.process_for_pdf()
    print(f"✅ PDF processing completed")
    print(f"   Section title: {pdf_data['section_title']}")
    print(f"   Section number: {pdf_data['section_number']}")

    return True


def test_manager_integration():
    """Test manager integration"""
    print("\n🧪 Testing Manager Integration...")

    manager = DemographicsManager()

    # Check if death registration is available
    categories = manager.get_available_categories()
    print(f"✅ Available categories: {categories}")

    if "death_registration" in categories:
        print("✅ Death registration processor is registered in manager")

        # Test processing through manager
        result = manager.process_category_for_pdf("death_registration")
        if result:
            print(f"✅ Manager processing successful")
            print(f"   Total deaths: {result['total_deaths']}")
        else:
            print("❌ Manager processing failed")
    else:
        print("❌ Death registration processor not found in manager")

    return True


if __name__ == "__main__":
    print("🚀 Starting Death Registration Tests...\n")

    try:
        test_death_registration()
        test_manager_integration()
        print("\n✅ All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
