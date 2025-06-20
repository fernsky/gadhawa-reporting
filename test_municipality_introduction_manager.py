#!/usr/bin/env python3
"""
Test script for Municipality Introduction Manager

Tests the manager functionality with all sections including historical background.
"""

import os
import sys
import django

# Add the project root directory to Python path
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.base")
django.setup()

from apps.municipality_introduction.processors.manager import (
    MunicipalityIntroductionManager,
)


def test_manager():
    """Test the municipality introduction manager"""
    print("=" * 80)
    print("TESTING MUNICIPALITY INTRODUCTION MANAGER")
    print("=" * 80)

    # Initialize manager
    manager = MunicipalityIntroductionManager()

    # Test available categories
    print(f"\n1. Available Categories:")
    categories = manager.get_available_categories()
    for i, category in enumerate(categories, 1):
        print(f"   {i}. {category}")

    # Test individual processors
    print(f"\n2. Testing Individual Processors:")
    for category in categories:
        processor = manager.get_processor(category)
        if processor:
            print(f"   ✅ {category}: {processor.__class__.__name__}")
            print(f"      Section: {processor.get_section_title()}")
            print(f"      Has Data: {processor.has_data()}")
        else:
            print(f"   ❌ {category}: No processor found")

    # Test processing all categories for PDF
    print(f"\n3. Processing All Categories for PDF:")
    try:
        all_results = manager.process_all_for_pdf()
        print(f"   ✅ Successfully processed {len(all_results)} categories")

        for category, result in all_results.items():
            print(f"   📄 {category}:")
            print(f"      Success: {result.get('success', 'N/A')}")
            if result.get("section_title"):
                print(f"      Title: {result['section_title']}")
            if result.get("section_number"):
                print(f"      Number: {result['section_number']}")
            if result.get("error"):
                print(f"      Error: {result['error']}")

    except Exception as e:
        print(f"   ❌ Error processing all categories: {str(e)}")
        import traceback

        traceback.print_exc()

    # Test processing specific category
    print(f"\n4. Testing Specific Category Processing:")
    for category in categories:
        try:
            result = manager.process_category_for_pdf(category)
            if result:
                print(f"   ✅ {category}: Success = {result.get('success', 'N/A')}")
            else:
                print(f"   ❌ {category}: No result returned")
        except Exception as e:
            print(f"   ❌ {category}: Error - {str(e)}")

    # Test data availability summary
    print(f"\n5. Data Availability Summary:")
    for category in categories:
        processor = manager.get_processor(category)
        if processor:
            summary = processor.get_data_summary()
            print(f"   📊 {category}:")
            print(f"      Records: {summary.get('record_count', 0)}")
            print(f"      Has Data: {summary.get('has_data', False)}")
            print(f"      Template: {summary.get('template', 'N/A')}")

    print("\n" + "=" * 80)
    print("MUNICIPALITY INTRODUCTION MANAGER TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    test_manager()
