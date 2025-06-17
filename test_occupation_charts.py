#!/usr/bin/env python3
"""
Test script to debug occupation chart generation
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.demographics.processors.occupation import OccupationProcessor


def test_occupation_charts():
    """Test occupation chart generation"""
    print("Testing occupation chart generation...")

    # Initialize processor
    processor = OccupationProcessor()

    # Get data
    print("Getting occupation data...")
    data = processor.get_data()

    print(f"Municipality data keys: {list(data['municipality_data'].keys())}")
    print(f"Ward data keys: {list(data['ward_data'].keys())}")

    # Print sample data
    print("\nSample municipality data:")
    for occ_type, occ_data in list(data["municipality_data"].items())[:3]:
        print(f"  {occ_type}: {occ_data}")

    print("\nSample ward data:")
    first_ward = list(data["ward_data"].keys())[0]
    ward_info = data["ward_data"][first_ward]
    print(f"Ward {first_ward}:")
    print(f"  Total population: {ward_info.get('total_population', 0)}")
    print(f"  Demographics keys: {list(ward_info['demographics'].keys())}")

    # Test chart generation
    print("\nTesting chart generation...")
    try:
        charts = processor.generate_and_save_charts(data)
        print(f"Generated charts: {charts}")

        # Test SVG generation directly
        print("\nTesting SVG generation...")
        pie_svg = processor.generate_chart_svg(data, chart_type="pie")
        print(f"Pie chart SVG length: {len(pie_svg) if pie_svg else 0}")

        bar_svg = processor.generate_chart_svg(data, chart_type="bar")
        print(f"Bar chart SVG length: {len(bar_svg) if bar_svg else 0}")

        if bar_svg:
            print("Bar chart SVG generated successfully!")
            # Save to file for inspection
            with open("test_bar_chart.svg", "w", encoding="utf-8") as f:
                f.write(bar_svg)
            print("Saved test bar chart to test_bar_chart.svg")
        else:
            print("Bar chart SVG generation failed!")

    except Exception as e:
        print(f"Error during chart generation: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_occupation_charts()
