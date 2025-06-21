#!/usr/bin/env python
"""
Quick test script to verify educational institution gender ratio calculations
"""
import os
import sys
import django

# Add the project root to Python path
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.social.processors.educational_institution import (
    EducationalInstitutionProcessor,
)


def test_gender_ratio_calculations():
    """Test the gender ratio calculations in the educational institution processor"""
    processor = EducationalInstitutionProcessor()
    data = processor.get_data()

    print("=== Educational Institution Gender Ratio Test ===")
    print(f"Total students: {data['total_students']}")
    print(f"Total male students: {data['total_male_students']}")
    print(f"Total female students: {data['total_female_students']}")
    print(f"Overall gender ratio: {data['gender_ratio']}% (female)")
    print()

    print("Municipality Data (by school level):")
    for level, level_data in data["municipality_data"].items():
        print(f"  {level_data['name_nepali']}:")
        print(f"    Total students: {level_data['total_students']}")
        print(f"    Male: {level_data['male_students']}")
        print(f"    Female: {level_data['female_students']}")
        print(f"    Gender ratio: {level_data['gender_ratio']}% (female)")
        print(f"    Percentage of total: {level_data['percentage']}%")
        print()

    print("Ward Data:")
    for ward_num, ward_data in data["ward_data"].items():
        print(f"  Ward {ward_num}:")
        print(f"    Total students: {ward_data['total_students']}")
        print(f"    Male: {ward_data['male_students']}")
        print(f"    Female: {ward_data['female_students']}")
        print(f"    Gender ratio: {ward_data['gender_ratio']}% (female)")
        print(f"    Number of institutions: {len(ward_data['institutions'])}")

        for inst in ward_data["institutions"][:3]:  # Show first 3 institutions
            print(f"      - {inst['name']}: {inst['gender_ratio']}% female")

        if len(ward_data["institutions"]) > 3:
            print(
                f"      ... and {len(ward_data['institutions']) - 3} more institutions"
            )
        print()

    print("Historical Data:")
    for year, hist_data in data["historical_data"].items():
        print(f"  Year {year}:")
        print(f"    Total students: {hist_data['total_students']}")
        print(f"    Gender ratio: {hist_data['gender_ratio']}% (female)")
        print()


if __name__ == "__main__":
    test_gender_ratio_calculations()
