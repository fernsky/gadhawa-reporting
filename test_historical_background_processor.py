#!/usr/bin/env python3
"""
Test script for Historical Background Processor

Tests the processor functionality for the २.२ ऐतिहासिक पृष्ठभूमि तथा नामाकरण section.
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

from apps.municipality_introduction.processors.historical_background import (
    HistoricalBackgroundProcessor,
)
from apps.municipality_introduction.models import HistoricalBackgroundInfo


def test_processor():
    """Test the historical background processor"""
    print("=" * 80)
    print("TESTING HISTORICAL BACKGROUND PROCESSOR")
    print("=" * 80)

    # Initialize processor
    processor = HistoricalBackgroundProcessor()

    # Test basic processor methods
    print(f"\n1. Section Identifier: {processor.get_section_identifier()}")
    print(f"2. Section Title: {processor.get_section_title()}")
    print(f"3. Template Name: {processor.get_template_name()}")
    print(f"4. Has Data: {processor.has_data()}")

    # Test data summary
    print(f"\n5. Data Summary:")
    summary = processor.get_data_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")

    # Test data processing
    print(f"\n6. Processing Data:")
    processed_data = processor.process_data()
    print(f"   Success: {processed_data.get('success', 'N/A')}")
    print(f"   Section: {processed_data.get('section', 'N/A')}")
    print(f"   Error: {processed_data.get('error', 'None')}")

    if processed_data.get("success"):
        data = processed_data["data"]
        print(f"   Municipality: {data.get('municipality_name', 'N/A')}")
        print(
            f"   Festivals: {len(data.get('cultural_heritage', {}).get('festivals', []))}"
        )
        print(
            f"   Languages: {len(data.get('cultural_heritage', {}).get('languages', []))}"
        )
        print(
            f"   Forest Types: {len(data.get('geographic_features', {}).get('forest_types', []))}"
        )
        print(
            f"   Religious Sites: {len(data.get('religious_heritage', {}).get('religious_sites', []))}"
        )

    # Test context for template
    print(f"\n7. Template Context:")
    context = processor.get_context_for_template()
    print(f"   Section Title: {context.get('section_title', 'N/A')}")
    print(f"   Municipality: {context.get('municipality_name', 'N/A')}")

    # Test validation
    print(f"\n8. Data Validation:")
    validation = processor.validate_data()
    print(f"   Is Valid: {validation['is_valid']}")
    print(f"   Errors: {len(validation['errors'])}")
    print(f"   Warnings: {len(validation['warnings'])}")
    print(f"   Summary: {validation['summary']}")

    if validation["errors"]:
        print("   Error Details:")
        for error in validation["errors"]:
            print(f"     - {error['message']}")

    if validation["warnings"]:
        print("   Warning Details:")
        for warning in validation["warnings"]:
            print(f"     - {warning['message']}")

    # Test raw data
    print(f"\n9. Raw Data Information:")
    if HistoricalBackgroundInfo.objects.exists():
        info = HistoricalBackgroundInfo.objects.first()
        print(f"   Record ID: {info.id}")
        print(f"   Formation Date: {info.formation_date}")
        print(f"   Main River: {info.main_river_name}")
        print(
            f"   Festivals: {', '.join(info.festivals_list[:3])}{'...' if len(info.festivals_list) > 3 else ''}"
        )
        print(f"   Languages: {', '.join(info.languages_list)}")
        print(
            f"   Forest Types: {', '.join(info.forest_types_list[:3])}{'...' if len(info.forest_types_list) > 3 else ''}"
        )
        print(
            f"   Religious Sites: {', '.join(info.religious_sites_list[:3])}{'...' if len(info.religious_sites_list) > 3 else ''}"
        )
        print(f"   Former VDCs: {len(info.former_vdcs_list)} गाविसहरू")

        # Test model properties
        print(f"\n10. Model Properties Test:")
        print(f"   Forest Types List: {info.forest_types_list}")
        print(f"   Festivals List: {info.festivals_list}")
        print(f"   Languages List: {info.languages_list}")
        print(f"   Religious Sites List: {info.religious_sites_list}")
        print(f"   Former VDCs List: {info.former_vdcs_list}")
    else:
        print("   No data found!")

    print("\n" + "=" * 80)
    print("HISTORICAL BACKGROUND PROCESSOR TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    test_processor()
