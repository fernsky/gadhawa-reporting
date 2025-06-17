#!/usr/bin/env python
"""
Test script for old age and single women processor
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

from apps.social.processors.old_age_and_single_women import (
    OldAgeAndSingleWomenProcessor,
)


def test_old_age_processor():
    print("=== Testing Old Age and Single Women Processor ===")

    # Initialize processor
    processor = OldAgeAndSingleWomenProcessor()
    print(f"✓ Processor initialized: {processor.get_section_title()}")
    print(f"✓ Section number: {processor.get_section_number()}")

    # Get data
    print("\n--- Getting Data ---")
    data = processor.get_data()

    print(f"Total elderly population: {data.get('total_old_age_population', 0):,}")
    print(f"Total male elderly: {data.get('total_male_old_age', 0):,}")
    print(f"Total female elderly: {data.get('total_female_old_age', 0):,}")
    print(f"Total single women: {data.get('total_single_women', 0):,}")
    print(f"Number of wards with data: {len(data.get('ward_data', {}))}")

    # Show municipality data
    print("\n--- Municipality Data ---")
    municipality_data = data.get("municipality_data", {})
    for key, value in municipality_data.items():
        print(
            f"{key}: {value['name_nepali']} - {value['population']:,} ({value['percentage']:.1f}%)"
        )

    # Show ward data sample
    print("\n--- Ward Data Sample ---")
    ward_data = data.get("ward_data", {})
    for ward_num in sorted(ward_data.keys())[:3]:  # Show first 3 wards
        ward_info = ward_data[ward_num]
        print(
            f"Ward {ward_num}: Male elderly: {ward_info['male_old_age_population']:,}, "
            f"Female elderly: {ward_info['female_old_age_population']:,}, "
            f"Total elderly: {ward_info['total_old_age_population']:,}"
        )

    # Generate analysis
    print("\n--- Analysis Text ---")
    analysis = processor.generate_analysis_text(data)
    print(f"Analysis length: {len(analysis)} characters")
    print(f"First 200 chars: {analysis[:200]}...")

    # Test PDF processing
    print("\n--- PDF Processing ---")
    try:
        pdf_data = processor.process_for_pdf()
        print(f"✓ PDF data generated successfully")
        print(f"✓ Section title: {pdf_data.get('section_title')}")
        print(f"✓ Section number: {pdf_data.get('section_number')}")
        print(f"✓ Has municipality data: {bool(pdf_data.get('municipality_data'))}")
        print(f"✓ Has ward data: {bool(pdf_data.get('ward_data'))}")
        print(f"✓ Has analysis: {bool(pdf_data.get('coherent_analysis'))}")
        print(f"✓ Has charts: {bool(pdf_data.get('pdf_charts'))}")

        # Check chart data
        charts = pdf_data.get("pdf_charts", {}).get("old_age_and_single_women", {})
        print(f"✓ Available charts: {list(charts.keys())}")
    except Exception as e:
        print(f"✗ Error in PDF processing: {e}")

    print("\n=== Old Age and Single Women Processor Test Complete ===")


if __name__ == "__main__":
    test_old_age_processor()
