#!/usr/bin/env python3
"""
Test script for demographics manager
"""
import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.demographics.processors.manager import get_demographics_manager


def test_demographics_manager():
    print("Testing DemographicsManager...")

    try:
        manager = get_demographics_manager()
        print("✓ Manager initialized successfully")

        # Test process_all_for_pdf
        all_data = manager.process_all_for_pdf()
        print(f"✓ All data processed successfully")

        # Check economically_active specifically
        if "economically_active" in all_data:
            econ_data = all_data["economically_active"]
            print("✓ Economically active data found")
            print(f"  - Data keys: {list(econ_data.keys())}")
            print(f"  - Total population: {econ_data.get('total_population', 0)}")
            print(f"  - Has data: {'data' in econ_data}")
            print(f"  - Has report_content: {'report_content' in econ_data}")
            print(f"  - Has charts: {'charts' in econ_data}")

            if "data" in econ_data:
                data = econ_data["data"]
                print(f"  - Data structure keys: {list(data.keys())}")
                print(f"  - Age group data: {len(data.get('age_group_data', {}))}")
                print(f"  - Ward data: {len(data.get('ward_data', {}))}")
        else:
            print("✗ Economically active data NOT found!")
            print(f"Available categories: {list(all_data.keys())}")

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_demographics_manager()
    if success:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Tests failed!")
