#!/usr/bin/env python
"""
Test script for economics manager
"""

import os
import sys
import django

# Add project root to sys.path
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")

# Setup Django
django.setup()

from apps.economics.processors.manager import get_economics_manager


def test_economics_manager():
    print("Testing Economics Manager...")

    # Initialize manager
    manager = get_economics_manager()

    # Test processor registry
    print(f"\n1. Available processors: {list(manager.processors.keys())}")

    # Test get_remittance_expenses_data
    print("\n2. Testing remittance expenses data...")
    try:
        remittance_data = manager.get_remittance_expenses_data()
        print(f"   Section title: {remittance_data.get('section_title')}")
        print(f"   Section number: {remittance_data.get('section_number')}")
        print(f"   Total households: {remittance_data.get('total_households')}")
        print(
            f"   Municipality data categories: {len(remittance_data.get('municipality_data', {}))}"
        )
        print(f"   Ward data: {len(remittance_data.get('ward_data', {}))}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test process_all_for_pdf
    print("\n3. Testing process_all_for_pdf...")
    try:
        all_data = manager.process_all_for_pdf()
        print(f"   Available sections: {list(all_data.keys())}")
        for section, data in all_data.items():
            print(f"     {section}: {data.get('total_households', 0)} households")
    except Exception as e:
        print(f"   Error: {e}")

    print("\n✅ Economics Manager test completed!")
    return True


if __name__ == "__main__":
    test_economics_manager()
