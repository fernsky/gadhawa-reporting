#!/usr/bin/env python3
"""
Test Religion Chart Caching with Data Changes

This script tests if the religion chart caching detects data changes properly.
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings")
django.setup()

from apps.demographics.processors.religion import ReligionProcessor


def test_religion_caching_with_changes():
    """Test religion chart caching with data changes"""
    print("🧪 Testing Religion Chart Caching with Data Changes...")
    print("=" * 60)

    processor = ReligionProcessor()

    # First run - should use existing charts or generate if needed
    print("\n🔄 First run:")
    result1 = processor.process_for_pdf()

    print(f"Charts: {list(result1['charts'].keys())}")
    print(f"Chart status: {result1['chart_management_status']}")

    # Manually modify the data to simulate a change
    print("\n🔧 Simulating data change...")
    original_get_data = processor.get_data

    def modified_get_data():
        data = original_get_data()
        # Add some fake population to Hindu religion to change the data
        if "HINDU" in data:
            data["HINDU"]["population"] += 100
            # Recalculate percentage
            total = sum(d["population"] for d in data.values())
            for religion, d in data.items():
                d["percentage"] = round((d["population"] / total) * 100, 2)
        return data

    # Replace the method temporarily
    processor.get_data = modified_get_data

    # Second run - should detect the change and regenerate charts
    print("\n🔄 Second run (with modified data):")
    result2 = processor.process_for_pdf()

    print(f"Charts: {list(result2['charts'].keys())}")
    print(f"Chart status: {result2['chart_management_status']}")

    # Restore original method
    processor.get_data = original_get_data

    # Third run - should use cached charts again
    print("\n🔄 Third run (with original data):")
    result3 = processor.process_for_pdf()

    print(f"Charts: {list(result3['charts'].keys())}")
    print(f"Chart status: {result3['chart_management_status']}")

    # Analysis
    print("\n📊 Analysis:")
    print(f"Run 1 vs Run 2 - Same data: {result1['data'] == result2['data']}")
    print(f"Run 1 vs Run 3 - Same data: {result1['data'] == result3['data']}")
    print(f"Run 2 charts current: {result2['chart_management_status']['all_current']}")
    print(f"Run 3 charts current: {result3['chart_management_status']['all_current']}")

    if not result2["chart_management_status"]["all_current"]:
        print("✅ Chart caching correctly detected data changes!")
    else:
        print("❌ Chart caching failed to detect data changes.")

    if result3["chart_management_status"]["all_current"]:
        print("✅ Chart caching correctly reused charts for same data!")
    else:
        print("❌ Chart caching failed to reuse charts for same data.")


if __name__ == "__main__":
    test_religion_caching_with_changes()
