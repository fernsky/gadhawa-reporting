#!/usr/bin/env python
"""
Test script for demographics manager with ward settlement
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

from apps.demographics.processors.manager import DemographicsManager


def test_demographics_manager():
    print("🧪 Testing Demographics Manager with Ward Settlement...")

    manager = DemographicsManager()

    # Test available categories
    categories = manager.get_available_categories()
    print(f"Available Categories: {categories}")

    # Test ward settlement processor
    ward_settlement_processor = manager.get_processor("ward_settlement")
    if ward_settlement_processor:
        print("✅ Ward Settlement processor found in manager")

        # Test processing for PDF
        pdf_data = manager.process_category_for_pdf("ward_settlement")
        if pdf_data:
            print(f"✅ Ward Settlement PDF processing successful")
            print(f"   Total Settlements: {pdf_data.get('total_settlements', 0)}")
            print(f"   Total Wards: {pdf_data.get('total_wards', 0)}")
        else:
            print("❌ Ward Settlement PDF processing failed")
    else:
        print("❌ Ward Settlement processor not found in manager")

    # Test processing all categories
    print(f"\n📊 Testing all categories processing...")
    all_results = manager.process_all_for_pdf()
    print(f"Processed categories: {list(all_results.keys())}")

    if "ward_settlement" in all_results:
        ward_result = all_results["ward_settlement"]
        print(f"✅ Ward Settlement included in all results")
        print(
            f"   Section: {ward_result.get('section_number', '')} {ward_result.get('section_title', '')}"
        )
        print(
            f"   Subsection: {ward_result.get('subsection_number', '')} {ward_result.get('subsection_title', '')}"
        )
    else:
        print("❌ Ward Settlement not found in all results")

    print("✅ Demographics Manager test completed!")


if __name__ == "__main__":
    test_demographics_manager()
