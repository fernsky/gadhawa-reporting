#!/usr/bin/env python
"""
Test High-Quality Religion Chart Generation

This script tests the updated religion processor with high-quality chart generation using Inkscape.
"""

import os
import django
from pathlib import Path

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.demographics.processors.religion import ReligionProcessor


def test_high_quality_chart_generation():
    """Test high-quality chart generation with Inkscape"""
    print("=== Testing High-Quality Religion Chart Generation ===\n")

    # Initialize processor
    processor = ReligionProcessor()
    print(f"✓ Religion processor initialized")
    print(f"✓ Chart key: {processor.get_chart_key()}")
    print(f"✓ Static charts directory: {processor.static_charts_dir}")

    # Get data
    print("\n--- Getting Religion Data ---")
    data = processor.get_data()
    print(f"✓ Retrieved data for {len(data)} religions")

    total_population = sum(
        item["population"]
        for item in data.values()
        if isinstance(item, dict) and "population" in item
    )
    print(f"✓ Total population: {total_population}")

    # Show religion breakdown
    print("\n--- Religion Breakdown ---")
    for religion_type, religion_data in data.items():
        if religion_data["population"] > 0:
            print(
                f"  {religion_data['name_nepali']}: {religion_data['population']} ({religion_data['percentage']:.1f}%)"
            )

    # Clear existing charts to force regeneration
    print("\n--- Clearing Existing Charts ---")
    from apps.chart_management.models import ChartFile

    deleted_count = ChartFile.objects.filter(
        chart_key__startswith="demographics_religion"
    ).delete()[0]
    print(f"✓ Deleted {deleted_count} existing chart records")

    # Test high-quality chart generation
    print("\n--- Testing High-Quality Chart Generation ---")
    try:
        charts = processor.generate_and_track_charts(data)
        print(f"✓ Chart generation completed")
        print(f"✓ Generated charts: {list(charts.keys())}")

        # Check if PNG files were created (high quality)
        if any(key.endswith("_png") for key in charts.keys()):
            print("🎉 HIGH-QUALITY PNG CHARTS GENERATED!")

            for key, value in charts.items():
                if key.endswith("_png"):
                    chart_path = processor.static_charts_dir / value
                    if chart_path.exists():
                        file_size = chart_path.stat().st_size
                        print(f"  📊 {key}: {value} ({file_size:,} bytes)")
                    else:
                        print(f"  ⚠ {key}: {value} (FILE NOT FOUND)")

        # Check URLs
        for key, value in charts.items():
            if key.endswith("_url"):
                print(f"  🔗 {key}: {value}")

    except Exception as e:
        print(f"⚠ Chart generation error: {e}")
        import traceback

        traceback.print_exc()

    # Test full PDF processing with high-quality charts
    print("\n--- Testing Full PDF Processing ---")
    try:
        pdf_data = processor.process_for_pdf()
        print(f"✓ PDF processing completed")
        print(f"✓ Charts in PDF data: {list(pdf_data['charts'].keys())}")

        # Check chart quality indicators
        if any(key.endswith("_png") for key in pdf_data["charts"].keys()):
            print("🎉 PDF WILL USE HIGH-QUALITY PNG CHARTS!")
        else:
            print("ℹ️ PDF will use SVG charts (fallback)")

    except Exception as e:
        print(f"⚠ PDF processing error: {e}")
        import traceback

        traceback.print_exc()

    # Check final chart files
    print("\n--- Final Chart Files ---")
    chart_dir = processor.static_charts_dir
    if chart_dir.exists():
        religion_files = list(chart_dir.glob("religion_*"))
        for file_path in sorted(religion_files):
            file_size = file_path.stat().st_size
            print(f"  📁 {file_path.name}: {file_size:,} bytes")
    else:
        print("  ⚠ Chart directory does not exist")

    print("\n=== High-Quality Chart Test Completed ===")


if __name__ == "__main__":
    test_high_quality_chart_generation()
