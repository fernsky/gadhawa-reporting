#!/usr/bin/env python
"""
Test script for Religion Chart Management Integration

This script tests the integration of chart management system with religion demographics.
"""

import os
import django
from pathlib import Path

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from apps.demographics.processors.religion import ReligionProcessor
from apps.chart_management.services import get_chart_service
from apps.chart_management.models import ChartFile


def test_religion_chart_management():
    """Test religion processor with chart management"""
    print("=== Testing Religion Chart Management Integration ===\n")

    # Initialize processor
    processor = ReligionProcessor()
    print(f"✓ Religion processor initialized")
    print(f"✓ Chart key: {processor.get_chart_key()}")

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

    # Test chart currency check
    print("\n--- Testing Chart Currency ---")
    chart_status = processor.check_charts_current(data)
    print(f"✓ Pie chart current: {chart_status['pie_current']}")
    print(f"✓ Bar chart current: {chart_status['bar_current']}")
    print(f"✓ All charts current: {chart_status['all_current']}")

    # Test chart generation and tracking
    print("\n--- Testing Chart Generation & Tracking ---")
    try:
        charts = processor.generate_and_track_charts(data)
        print(f"✓ Generated charts: {list(charts.keys())}")

        if "pie_chart_url" in charts:
            print(f"✓ Pie chart URL: {charts['pie_chart_url']}")
        if "bar_chart_url" in charts:
            print(f"✓ Bar chart URL: {charts['bar_chart_url']}")

    except Exception as e:
        print(f"⚠ Chart generation error: {e}")

    # Test getting existing chart URLs
    print("\n--- Testing Chart URL Retrieval ---")
    pie_url = processor.get_chart_url("pie")
    bar_url = processor.get_chart_url("bar")
    print(f"✓ Pie chart URL from service: {pie_url}")
    print(f"✓ Bar chart URL from service: {bar_url}")

    # Test full PDF processing
    print("\n--- Testing Full PDF Processing ---")
    try:
        pdf_data = processor.process_for_pdf()
        print(f"✓ PDF processing completed")
        print(f"✓ Section title: {pdf_data['section_title']}")
        print(f"✓ Section number: {pdf_data['section_number']}")
        print(f"✓ Total population: {pdf_data['total_population']}")
        print(f"✓ Charts available: {list(pdf_data['charts'].keys())}")
        print(f"✓ Chart management status: {pdf_data['chart_management_status']}")

    except Exception as e:
        print(f"⚠ PDF processing error: {e}")

    # Show chart management database records
    print("\n--- Chart Management Database Records ---")
    chart_files = ChartFile.objects.filter(
        chart_key__startswith="demographics_religion"
    )
    print(f"✓ Found {chart_files.count()} chart records in database")

    for chart_file in chart_files:
        print(
            f"  - {chart_file.chart_key} ({chart_file.chart_type}): {chart_file.file_path}"
        )
        print(f"    Exists: {chart_file.exists()}, URL: {chart_file.url}")

    print("\n=== Test Completed ===")


if __name__ == "__main__":
    test_religion_chart_management()
