#!/usr/bin/env python
"""
Test script to debug major subject ward-wise data display
"""

import os
import django
import sys

# Add project path
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.social.processors.major_subject import MajorSubjectProcessor


def test_major_subject_ward_data():
    """Test major subject processor ward data formatting"""
    print("=" * 60)
    print("TESTING MAJOR SUBJECT WARD DATA")
    print("=" * 60)

    processor = MajorSubjectProcessor()
    data = processor.get_data()

    print(f"\nTotal population: {data.get('total_population', 0)}")
    print(f"Municipality data keys: {list(data.get('municipality_data', {}).keys())}")
    print(f"Ward data keys: {list(data.get('ward_data', {}).keys())}")

    # Check raw ward data structure
    if data.get("ward_data"):
        print("\n" + "=" * 40)
        print("RAW WARD DATA STRUCTURE:")
        print("=" * 40)
        for ward_num, ward_data in data["ward_data"].items():
            print(f"\nWard {ward_num}:")
            print(f"  - ward_number: {ward_data.get('ward_number')}")
            print(f"  - ward_name: {ward_data.get('ward_name')}")
            print(f"  - total_population: {ward_data.get('total_population')}")
            print(f"  - subjects keys: {list(ward_data.get('subjects', {}).keys())}")

            # Show first few subjects for verification
            subjects = ward_data.get("subjects", {})
            for i, (subject_code, subject_data) in enumerate(subjects.items()):
                if i < 3:  # Show first 3
                    print(f"    - {subject_code}: {subject_data}")

    # Test process_for_pdf to see formatted data
    print("\n" + "=" * 40)
    print("TESTING PROCESS_FOR_PDF (FORMATTED DATA):")
    print("=" * 40)

    formatted_data = processor.process_for_pdf()
    formatted_ward_data = formatted_data.get("ward_data", {})

    if formatted_ward_data:
        print(f"Formatted ward data keys: {list(formatted_ward_data.keys())}")

        for ward_num, ward_info in formatted_ward_data.items():
            print(f"\nFormatted Ward {ward_num}:")
            print(f"  - total_population: {ward_info.get('total_population')}")

            # Check if demographics field exists
            demographics = ward_info.get("demographics", {})
            print(f"  - demographics keys: {list(demographics.keys())}")

            # Show first few demographics entries
            for i, (demo_key, demo_data) in enumerate(demographics.items()):
                if i < 3:  # Show first 3
                    print(f"    - {demo_key}: {demo_data}")

            # Also check if subjects field still exists
            subjects = ward_info.get("subjects", {})
            print(f"  - subjects keys: {list(subjects.keys())}")

            if i >= 2:  # Only show details for first few wards
                break

    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    test_major_subject_ward_data()
