#!/usr/bin/env python
"""
Test script for remittance expenses processor
"""

import os
import sys
import django

# Add project root to sys.path
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")

# Setup Django
django.setup()

from apps.economics.processors.remittance_expenses import RemittanceExpensesProcessor


def test_remittance_expenses_processor():
    print("Testing Remittance Expenses Processor...")

    # Initialize processor
    processor = RemittanceExpensesProcessor()

    # Test get_data method
    print("\n1. Testing get_data method...")
    data = processor.get_data()

    print(f"   Municipality data keys: {list(data['municipality_data'].keys())}")
    print(f"   Total households: {data['total_households']}")
    print(f"   Number of wards: {len(data['ward_data'])}")

    # Test analysis generation
    print("\n2. Testing analysis generation...")
    analysis = processor.generate_analysis_text(data)
    print(f"   Analysis length: {len(analysis)} characters")
    print(f"   Analysis preview: {analysis[:200]}...")

    # Test chart generation
    print("\n3. Testing chart generation...")
    try:
        chart_svg = processor.generate_pie_chart(data["municipality_data"])
        print(f"   Chart generated successfully: {len(chart_svg)} characters")
    except Exception as e:
        print(f"   Chart generation error: {e}")

    # Test PDF processing
    print("\n4. Testing process_for_pdf...")
    try:
        pdf_data = processor.process_for_pdf()
        print(f"   PDF data keys: {list(pdf_data.keys())}")
        print(f"   Municipality data available: {'municipality_data' in pdf_data}")
        print(f"   Ward data available: {'ward_data' in pdf_data}")
        print(f"   Charts available: {'pdf_charts' in pdf_data}")
    except Exception as e:
        print(f"   PDF processing error: {e}")

    print("\n✅ Remittance Expenses Processor test completed!")
    return True


if __name__ == "__main__":
    test_remittance_expenses_processor()
