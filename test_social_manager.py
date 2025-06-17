#!/usr/bin/env python
"""
Test script for social manager integration
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.social.processors.manager import get_social_manager


def test_social_manager():
    print("=== Testing Social Manager Integration ===")

    # Get social manager
    social_manager = get_social_manager()
    print(f"✓ Social manager initialized")
    print(f"✓ Available processors: {list(social_manager.processors.keys())}")

    # Test all processors
    print("\n--- Testing Individual Processors ---")
    for category, processor in social_manager.processors.items():
        print(f"\nTesting {category}:")
        try:
            data = processor.get_data()
            section_title = processor.get_section_title()
            section_number = processor.get_section_number()

            print(f"  ✓ Section: {section_number} - {section_title}")
            print(f"  ✓ Data keys: {list(data.keys())}")

            # Test some data presence
            if category == "old_age_and_single_women":
                total_elderly = data.get("total_old_age_population", 0)
                ward_count = len(data.get("ward_data", {}))
                print(f"  ✓ Total elderly: {total_elderly:,}")
                print(f"  ✓ Wards with data: {ward_count}")

        except Exception as e:
            print(f"  ✗ Error: {e}")

    # Test process_all_for_pdf
    print("\n--- Testing PDF Processing ---")
    try:
        pdf_data = social_manager.process_all_for_pdf()
        print(f"✓ PDF processing successful")
        print(f"✓ Categories processed: {list(pdf_data.keys())}")

        # Check old age and single women specifically
        if "old_age_and_single_women" in pdf_data:
            old_age_data = pdf_data["old_age_and_single_women"]
            print(f"✓ Old age data keys: {list(old_age_data.keys())}")

            # Check required fields for template
            required_fields = [
                "municipality_data",
                "single_women_data",
                "ward_data",
                "total_male_old_age",
                "total_female_old_age",
                "total_old_age_population",
                "total_single_women",
                "coherent_analysis",
                "pdf_charts",
            ]

            missing_fields = []
            for field in required_fields:
                if field not in old_age_data:
                    missing_fields.append(field)

            if missing_fields:
                print(f"  ✗ Missing fields: {missing_fields}")
            else:
                print(f"  ✓ All required fields present for template")

            # Check chart data
            charts = old_age_data.get("pdf_charts", {}).get(
                "old_age_and_single_women", {}
            )
            if charts:
                print(f"  ✓ Charts available: {list(charts.keys())}")
            else:
                print(f"  ✗ No charts available")

    except Exception as e:
        print(f"✗ PDF processing error: {e}")
        import traceback

        traceback.print_exc()

    # Test chart generation
    print("\n--- Testing Chart Generation ---")
    try:
        chart_urls = social_manager.generate_all_charts()
        print(f"✓ Chart generation successful")
        print(f"✓ Categories with charts: {list(chart_urls.keys())}")

        for category, charts in chart_urls.items():
            print(f"  {category}: {list(charts.keys())}")

    except Exception as e:
        print(f"✗ Chart generation error: {e}")

    print("\n=== Social Manager Integration Test Complete ===")


if __name__ == "__main__":
    test_social_manager()
