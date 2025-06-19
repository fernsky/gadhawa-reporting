#!/usr/bin/env python
"""
Debug the _extract_demographics_from_ward method
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


def debug_extract_demographics():
    """Debug the _extract_demographics_from_ward method"""
    print("=" * 60)
    print("DEBUGGING _extract_demographics_from_ward")
    print("=" * 60)

    processor = MajorSubjectProcessor()
    data = processor.get_data()

    # Get first ward data
    ward_data = data.get("ward_data", {})
    if ward_data:
        first_ward = list(ward_data.values())[0]
        print(f"First ward data structure:")
        print(f"  Keys: {list(first_ward.keys())}")
        print(f"  Ward number: {first_ward.get('ward_number')}")
        print(f"  Total population: {first_ward.get('total_population')}")

        # Check subjects field
        subjects = first_ward.get("subjects", {})
        print(f"  Subjects field exists: {'subjects' in first_ward}")
        print(f"  Subjects keys: {list(subjects.keys())}")

        # Manually test the extraction logic
        print("\n" + "=" * 40)
        print("MANUAL EXTRACTION TEST:")
        print("=" * 40)

        demographics = {}

        # Simulate the extraction logic
        print(
            f"Checking if 'toilet_types' in ward_info: {'toilet_types' in first_ward}"
        )
        print(
            f"Checking if 'waste_methods' in ward_info: {'waste_methods' in first_ward}"
        )
        print(f"Checking if 'subjects' in ward_info: {'subjects' in first_ward}")

        if "subjects" in first_ward:
            print("  Found subjects field, extracting...")
            for subject, subject_data in first_ward["subjects"].items():
                demographics[subject] = {
                    "name_nepali": subject_data.get("name_nepali", subject),
                    "population": subject_data.get("population", 0),
                    "percentage": subject_data.get("percentage", 0),
                }
            print(f"  Extracted demographics keys: {list(demographics.keys())}")
            print(f"  First few demographics:")
            for i, (key, value) in enumerate(demographics.items()):
                if i < 3:
                    print(f"    {key}: {value}")

        # Now test the actual method
        print("\n" + "=" * 40)
        print("ACTUAL METHOD TEST:")
        print("=" * 40)

        actual_demographics = processor._extract_demographics_from_ward(first_ward)
        print(f"Actual method result keys: {list(actual_demographics.keys())}")
        print(f"Actual method result:")
        for key, value in actual_demographics.items():
            print(f"  {key}: {value}")

        # Test with simplified ward info
        print("\n" + "=" * 40)
        print("SIMPLIFIED WARD INFO TEST:")
        print("=" * 40)

        simple_ward = {
            "ward_number": 1,
            "ward_name": "वडा नं. १",
            "total_population": 100,
            "subjects": {
                "ENGLISH": {
                    "name_nepali": "अंग्रेजी",
                    "population": 10,
                    "percentage": 10.0,
                },
                "NEPALI": {
                    "name_nepali": "नेपाली",
                    "population": 20,
                    "percentage": 20.0,
                },
            },
        }

        simple_result = processor._extract_demographics_from_ward(simple_ward)
        print(f"Simple test result keys: {list(simple_result.keys())}")
        print(f"Simple test result: {simple_result}")


if __name__ == "__main__":
    debug_extract_demographics()
