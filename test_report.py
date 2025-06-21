#!/usr/bin/env python
"""
Quick test script to verify educational institution report generation
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


def test_report_generation():
    """Test the report generation with gender ratio"""
    processor = EducationalInstitutionProcessor()
    report_data = processor.process_for_pdf()

    print("=== Educational Institution Report Test ===")
    print(f"Section title: {report_data['section_title']}")
    print(f"Total students: {report_data['total_students']}")
    print(f"Overall gender ratio: {report_data['gender_ratio']}%")
    print()

    # Check if analysis text contains gender ratio information
    analysis = report_data["coherent_analysis"]
    if "gender_ratio" in str(report_data["gender_ratio"]):
        print("✓ Gender ratio is being calculated correctly")
    else:
        print("✗ Gender ratio calculation issue")

    # Check analysis text length
    if len(analysis) > 1000:
        print("✓ Analysis text generated successfully")
        print(f"Analysis text length: {len(analysis)} characters")
    else:
        print("✗ Analysis text seems too short")

    # Check if municipality data has gender ratios
    has_gender_ratios = all(
        "gender_ratio" in level_data
        for level_data in report_data["municipality_data"].values()
    )

    if has_gender_ratios:
        print("✓ Municipality data has gender ratios for all levels")
    else:
        print("✗ Some municipality data missing gender ratios")

    # Check if ward data has gender ratios
    ward_has_gender_ratios = all(
        "gender_ratio" in ward_data for ward_data in report_data["ward_data"].values()
    )

    if ward_has_gender_ratios:
        print("✓ Ward data has gender ratios")
    else:
        print("✗ Ward data missing gender ratios")

    print("\nSample of municipality data:")
    for level, data in list(report_data["municipality_data"].items())[:2]:
        print(f"  {data['name_nepali']}: {data['gender_ratio']}% female")


if __name__ == "__main__":
    test_report_generation()
