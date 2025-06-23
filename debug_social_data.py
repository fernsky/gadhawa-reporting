#!/usr/bin/env python
"""
Test script to debug social domain data issues.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gadhawa_report.settings.development")
django.setup()

from apps.social.processors.toilet_type import ToiletTypeProcessor
from apps.social.models import WardWiseToiletType, ToiletTypeChoice


def debug_social_data():
    """Debug social domain data issues"""
    print("Debugging Social Domain Data Issues...")
    print("=" * 60)

    # Test 1: Check database contents
    print("1. Database Contents Check:")
    toilet_count = WardWiseToiletType.objects.count()
    print(f"   Total toilet type records: {toilet_count}")

    if toilet_count > 0:
        print("   Sample records:")
        for record in WardWiseToiletType.objects.all()[:5]:
            print(
                f"     Ward {record.ward_number}: {record.toilet_type} = {record.households} households"
            )

    # Test 2: Check enum mappings
    print("\n2. Enum Mappings Check:")
    print("   ToiletTypeChoice.choices:")
    for choice in ToiletTypeChoice.choices:
        print(f"     {choice[0]} -> {choice[1]}")

    # Test 3: Test processor data retrieval
    print("\n3. Processor Data Retrieval:")
    processor = ToiletTypeProcessor()
    try:
        data = processor.get_data()
        print(
            f"   Municipality data keys: {list(data.get('municipality_data', {}).keys())}"
        )
        print(f"   Ward data keys: {list(data.get('ward_data', {}).keys())}")
        print(f"   Total households: {data.get('total_households', 0)}")

        # Check municipality data structure
        if data.get("municipality_data"):
            print("\n   Municipality data structure:")
            for key, value in data["municipality_data"].items():
                print(f"     {key}: {value}")

        # Check ward data structure
        if data.get("ward_data"):
            print("\n   Ward data structure:")
            for ward_num, ward_info in data["ward_data"].items():
                print(f"     Ward {ward_num}:")
                print(f"       Total: {ward_info.get('total_population', 0)}")
                if "toilet_types" in ward_info:
                    for toilet_type, toilet_data in ward_info["toilet_types"].items():
                        print(f"       {toilet_type}: {toilet_data}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 4: Check chart data formatting
    print("\n4. Chart Data Formatting:")
    try:
        # Test municipality data formatting
        formatted_muni = processor._format_municipality_data_for_pie_chart(
            data.get("municipality_data", {})
        )
        print(f"   Formatted municipality data: {formatted_muni}")

        # Test ward data formatting
        formatted_ward = processor._format_ward_data_for_bar_chart(
            data.get("ward_data", {})
        )
        print(f"   Formatted ward data keys: {list(formatted_ward.keys())}")
        for ward_key, ward_data in formatted_ward.items():
            print(
                f"     Ward {ward_key}: {ward_data.get('total_population', 0)} total, {len(ward_data.get('demographics', {}))} demographics"
            )
    except Exception as e:
        print(f"   Error: {e}")

    print("\n" + "=" * 60)
    print("Debug Complete!")


if __name__ == "__main__":
    debug_social_data()
